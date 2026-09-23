"""Portable, opt-in CrossOver launcher; no patch installation or registry edits."""
import json
import os
from pathlib import Path
import subprocess
import sys

WINE = Path('Contents/SharedSupport/CrossOver/bin/wine')
GAME_REL = Path('drive_c/Program Files (x86)/Steam/steamapps/common/The Rhapsody of Zephyr Remastered')


def defaults(home):
    apps = [home / 'Applications/CrossOver.app', Path('/Applications/CrossOver.app')]
    bottles = home / 'Library/Application Support/CrossOver/Bottles'
    found = sorted(p for p in bottles.glob('*') if (p / 'cxbottle.conf').is_file())
    bottle = next((p for p in found if (p / GAME_REL / 'ZephyrRemastered.exe').is_file()),
                  found[0] if found else bottles / 'Steam')
    return dict(app=str(next((p for p in apps if (p / WINE).is_file()), apps[0])),
                bottle=str(bottle), game=str(bottle / GAME_REL))


def load_settings(path, fallback):
    try:
        saved = json.loads(path.read_text())
        return {k: saved[k] if isinstance(saved.get(k), str) else v for k, v in fallback.items()}
    except (OSError, ValueError, AttributeError):
        return fallback.copy()


def launch_args(settings):
    paths = {k: Path(settings[k]).expanduser().resolve() for k in ('app', 'bottle', 'game')}
    app, bottle, game = (paths[k] for k in ('app', 'bottle', 'game'))
    for p in (app / WINE, bottle / 'cxbottle.conf', bottle / 'system.reg',
              game / 'ZephyrRemastered.exe'):
        if not p.is_file():
            raise ValueError(f'Required file not found:\n{p}')
    if not os.access(app / WINE, os.X_OK):
        raise ValueError('The selected CrossOver Wine launcher is not executable.')
    # Map through the selected bottle's drives, including custom Steam libraries.
    # Prefer C: over Z: when both map the game. No shell command construction.
    drives = bottle / 'dosdevices'
    mappings = sorted(drives.glob('[a-z]:'), key=lambda p: (p.name != 'c:', p.name == 'z:', p.name))
    for drive in mappings:
        try:
            relative = (game / 'ZephyrRemastered.exe').relative_to(drive.resolve())
        except ValueError:
            continue
        exe = drive.name.upper() + '\\' + str(relative).replace('/', '\\')
        break
    else:
        raise ValueError('The game folder is not accessible through this bottle’s drives.\n'
                         'Choose the bottle that runs this game in CrossOver.')
    return [str(app / WINE), '--bottle', str(bottle), '--no-update',
            '--dll', 'winhttp=n,b', '--workdir', str(game), exe]


def main():
    if sys.platform != 'darwin':
        raise SystemExit('This launcher is for macOS / CrossOver only.')
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk

    home = Path.home()
    state = home / 'Library/Application Support/ZephyrEnglishPatcher'
    config = state / 'crossover-launcher.json'
    root = tk.Tk()
    root.title('Launch Zephyr — CrossOver')
    root.minsize(650, 350)
    box = ttk.Frame(root, padding=18)
    box.pack(fill='both', expand=True)
    ttk.Label(box, text='Launch your installed Steam game with mods', font=('', 16, 'bold')).grid(
        row=0, column=0, columnspan=3, sticky='w', pady=(0, 12))
    ttk.Label(box, text='Keep Steam open in the selected bottle and close other Zephyr copies.\n'
              'Clear the Linux/Proton command from Steam’s Launch Options.\n'
              'This launcher uses winhttp=n,b for this launch. It does not install mods or translations.',
              wraplength=650).grid(row=1, column=0, columnspan=3, sticky='w', pady=(0, 12))
    values = {k: tk.StringVar(value=v) for k, v in load_settings(config, defaults(home)).items()}

    def browse(key):
        current = Path(values[key].get()).expanduser()
        picker = filedialog.askopenfilename if key == 'app' else filedialog.askdirectory
        options = {'filetypes': [('CrossOver application', '*.app')]} if key == 'app' else {'mustexist': True}
        selected = picker(parent=root, title={
            'app': 'Select CrossOver.app', 'bottle': 'Select the bottle folder containing cxbottle.conf',
            'game': 'Select the folder containing ZephyrRemastered.exe'}[key],
            initialdir=str(current.parent if key == 'app' else current), **options)
        if selected:
            values[key].set(selected)
            if key == 'bottle' and (Path(selected) / GAME_REL / 'ZephyrRemastered.exe').is_file():
                values['game'].set(str(Path(selected) / GAME_REL))

    for row, (key, label) in enumerate((('app', 'CrossOver.app'), ('bottle', 'Bottle folder'),
                                       ('game', 'Game folder')), 2):
        ttk.Label(box, text=label).grid(row=row, column=0, sticky='w', padx=(0, 10), pady=6)
        ttk.Entry(box, textvariable=values[key], width=55).grid(row=row, column=1, sticky='ew')
        ttk.Button(box, text='Browse…', command=lambda k=key: browse(k)).grid(row=row, column=2, padx=(8, 0))
    box.columnconfigure(1, weight=1)
    status = tk.StringVar(value='Selections are remembered after a successful launch request.')
    ttk.Label(box, textvariable=status, wraplength=650).grid(row=5, column=0, columnspan=3, sticky='w', pady=12)

    def launch():
        settings = {k: v.get().strip() for k, v in values.items()}
        try:
            args = launch_args(settings)
            game = Path(settings['game']).expanduser()
            if (game / 'BepInEx').exists() and not (game / 'winhttp.dll').is_file():
                raise ValueError('BepInEx is installed but winhttp.dll is missing.\n'
                                 'Install the original mod loader in this game folder first.')
            state.mkdir(parents=True, exist_ok=True)
            logpath = state / 'crossover-launch.log'
            with logpath.open('w') as log:
                proc = subprocess.Popen(args, stdout=log, stderr=subprocess.STDOUT)
            temp = config.with_suffix('.tmp')
            temp.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + '\n')
            temp.replace(config)
        except (OSError, ValueError) as exc:
            messagebox.showerror('Cannot launch', str(exc), parent=root)
            return
        button.configure(state='disabled')
        status.set('Launch requested. Mod startup can take a few minutes. You may close this window.')

        def poll():
            code = proc.poll()
            if code is None:
                root.after(1000, poll)
            else:
                button.configure(state='normal')
                status.set(f'Launcher exited ({code}). Log: {logpath}')
                if code:
                    messagebox.showerror('CrossOver launch failed', f'Exit code {code}.\nSee {logpath}', parent=root)
        root.after(1000, poll)

    button = ttk.Button(box, text='Launch game', command=launch)
    button.grid(row=6, column=0, columnspan=3, sticky='e')
    root.mainloop()


if __name__ == '__main__':
    main()
