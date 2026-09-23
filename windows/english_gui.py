"""Offline single-executable English patcher UI."""
import sys
import os
import gzip
import json
import queue
import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from english_engine import Patcher, payload_default
from english_version import VERSION
from english_resources import sha
from english_trust import HASHES


from english_saves import prepare_saves


def main():
    if sys.platform == 'darwin' and tk.TkVersion < 8.6:
        raise RuntimeError('macOS GUI requires Tk 8.6 or newer. Use a current python.org Python or the packaged Mac app.')
    root = tk.Tk()
    manifest = json.loads((payload_default()/'manifest.json').read_text(encoding='utf8'))
    purple = manifest.get('platform') == 'purple'
    root.title('Zephyr English Patcher '+VERSION+(' — PURPLE experimental' if purple else ''))
    show_folder_help = sys.platform in ('win32', 'darwin')
    root.geometry('820x810' if sys.platform == 'win32' else '820x740' if show_folder_help else '760x600')
    root.minsize(800,790) if sys.platform == 'win32' else root.minsize(800,720) if show_folder_help else root.minsize(740,580)
    box = ttk.Frame(root,padding=20)
    box.pack(fill='both',expand=True)
    ttk.Label(box,text='The Rhapsody of Zephyr Remastered',font=('TkDefaultFont',17,'bold')).pack(anchor='w')
    ttk.Label(box,text='English playtest patch • 2.5× dialogue reveal • Original backups and restoration').pack(anchor='w',pady=(5,16))
    compatibility = ttk.LabelFrame(box, text='PURPLE edition — experimental' if purple else 'Compatible user mods', padding=10)
    compatibility.pack(fill='x',pady=(0,12))
    if purple:
        ttk.Label(compatibility,text='For the verified PURPLE game build only. Steam editions are not supported by this package.\nStandard translation; Fullmap and Passives compatibility is not verified on PURPLE.\nInstaller validation does not replace gameplay testing. Use a separate game copy first.',wraplength=710,justify='left').pack(anchor='w')
    else:
        ttk.Label(compatibility,text='Full Map: ZephyrFullmap 1.8.0  •  Passives: ZephyrPassives 2.4.3',wraplength=710,justify='left').pack(anchor='w')
        ttk.Label(compatibility,text='Automatically selects standard or Passives descriptions and translates installed Fullmap labels.\nMods are optional and must be installed separately. Unsupported mod versions use standard translation; mod files are preserved.',wraplength=710,justify='left').pack(anchor='w',pady=(4,0))
    ttk.Label(box,text='Choose the folder containing ZephyrRemastered.exe. Close the game first.').pack(anchor='w')
    default_game = None
    if purple:
        typical_game = r'C:\Program Files (x86)\NC\Rhapsody of Zephyr Remastered'
        if sys.platform == 'win32':
            default_game = Path(os.environ.get('ProgramFiles(x86)', r'C:\Program Files (x86)')) / 'NC' / 'Rhapsody of Zephyr Remastered'
        ttk.Label(box,text='Default PURPLE folder on Windows:\n'+typical_game+'\nInstalled elsewhere? Browse to the folder containing ZephyrRemastered.exe.\nKeep the PURPLE launcher available for authentication when testing.',wraplength=730,justify='left').pack(anchor='w',pady=(8,4))
    elif sys.platform == 'win32':
        default_game = Path(os.environ.get('ProgramFiles(x86)', r'C:\Program Files (x86)')) / 'Steam' / 'steamapps' / 'common' / 'The Rhapsody of Zephyr Remastered'
        ttk.Label(box,text='Usual Steam game folder:\n'+str(default_game),wraplength=730,justify='left').pack(anchor='w',pady=(8,4))
        ttk.Label(box,text='Installed on another drive? In Steam, right-click the game → Manage → Browse local files.\nCopy that folder address and paste it below, or select it with Browse.',wraplength=730,justify='left').pack(anchor='w')
    elif sys.platform == 'darwin':
        typical_game = '~/Library/Application Support/CrossOver/Bottles/Steam/drive_c/Program Files (x86)/Steam/steamapps/common/The Rhapsody of Zephyr Remastered'
        default_game = Path(typical_game).expanduser()
        ttk.Label(box,text='Typical CrossOver game folder (bottle named Steam):\n'+typical_game,wraplength=730,justify='left').pack(anchor='w',pady=(8,4))
        ttk.Label(box,text='Different bottle or location? In CrossOver, select your bottle → Open C: Drive, then find\nProgram Files (x86)/Steam/steamapps/common and select the game folder with Browse.\nIn the folder picker, press Shift+Command+G to paste a path (~ means your home folder).',wraplength=730,justify='left').pack(anchor='w')
    if sys.platform == 'win32':
        ttk.Label(box,text='Windows permissions: for a protected folder such as Program Files (x86), right-click\nthe patcher EXE → Run as administrator. After a failed install, use Check Files;\nif recovery is required, click Recover before trying Install English again.',wraplength=730,justify='left').pack(anchor='w',pady=(8,0))
    path = tk.StringVar()
    row=ttk.Frame(box);row.pack(fill='x',pady=8)
    entry=ttk.Entry(row,textvariable=path);entry.pack(side='left',fill='x',expand=True)
    buttons=[]
    def browse():
        options = {'initialdir': str(default_game)} if default_game and default_game.is_dir() else {}
        folder=filedialog.askdirectory(title='Select folder containing ZephyrRemastered.exe', **options)
        if folder:path.set(folder)
    browse_button=ttk.Button(row,text='Browse…',command=browse);browse_button.pack(side='right',padx=(8,0));buttons.append(browse_button)
    status=tk.StringVar(value='1. Select the game folder.  2. Click Check Files.  3. Click Install English.\nFor initial testing, select a separate game copy.')
    ttk.Label(box,textvariable=status,wraplength=650,justify='left').pack(anchor='w',pady=12)
    progress=ttk.Progressbar(box,mode='indeterminate');progress.pack(fill='x',pady=5)
    actions=ttk.Frame(box);actions.pack(fill='x',pady=12)
    results=queue.Queue();busy=False
    def start(work):
        nonlocal busy
        if busy:return
        busy=True
        for b in buttons:b.configure(state='disabled')
        entry.configure(state='disabled');progress.start();status.set('Working… Please leave the game closed.')
        def run():
            try:results.put((True,work()))
            except PermissionError as ex:
                help_text = ('Windows denied file access. Close the game and this patcher, then right-click the patcher EXE → Run as administrator. Select the same game folder and click Check Files. If recovery is required, click Recover, then Check Files before retrying Install English.\n\n' if sys.platform == 'win32' else '')
                results.put((False,help_text+str(ex)))
            except Exception as ex:results.put((False,str(ex)))
        threading.Thread(target=run,daemon=False).start()
    def operation(action):
        selected=path.get().strip()
        if not selected:
            messagebox.showinfo('Select game folder','Browse to the game folder first.');return
        selected=str(Path(selected).expanduser())
        if action in ('install','restore','recover'):
            text={'install':'Install the English playtest patch here? Original resources will be backed up. Saves are not changed.','restore':'Restore original game resources from this patcher\'s verified backup? Saves are not changed.','recover':'Recover the interrupted patch operation using its verified transaction backup?'}[action]
            if not messagebox.askyesno('Confirm',text+'\n\n'+selected):return
        def work():
            patcher=Patcher(selected)
            result=getattr(patcher,action)()
            labels={'original':'Supported original files. Ready to install.','installed':'English patch installed and verified.','unmanaged_localization':'English files exist, but this patcher has no managed backup. Use an original game copy.','unsupported_or_modified':'Unsupported version or modified files. No files were changed.','recovery_required':'An interrupted operation needs recovery.','update_available':'A managed English installation can be updated.'}
            return labels.get(result['status'],result['status'])+'\n'+result.get('translation_profile','')+' | '+'; '.join(result.get('detected_mods',[]))+'\nBackup files: '+str(result.get('backup_files',0))+'\n'+str(result.get('compatibility_reason') or '')
        start(work)
    for label,action in [('Check Files','status'),('Install English','install'),('Restore Original','restore'),('Recover','recover')]:
        b=ttk.Button(actions,text=label,command=lambda a=action:operation(a));b.pack(side='left',padx=(0,8));buttons.append(b)
    def saves():
        source=filedialog.askdirectory(title='Select ZephyrRemastered save folder (source stays unchanged)')
        if not source:return
        parent=filedialog.askdirectory(title='Select an OUTSIDE folder for converted copies')
        if not parent:return
        output=Path(parent)/('English Save Copies '+time.strftime('%Y%m%d-%H%M%S'))
        def work():
            file=payload_default()/'save-names.json'
            if sha(file)!=HASHES['save-names.json']:raise ValueError('Save-name data checksum failed.')
            return prepare_saves(source,output,json.loads(file.read_text(encoding='utf8')))
        start(work)
    b=ttk.Button(box,text='Prepare English save-name copies (optional)',command=saves);b.pack(anchor='w');buttons.append(b)
    ttk.Label(box,text='Experimental translation: some names and layouts remain under review.\nNo downloads or automatic updates. Keep this patcher for restoration.',wraplength=650).pack(anchor='w',pady=(14,0))
    def poll():
        nonlocal busy
        try:
            ok,text=results.get_nowait();busy=False;progress.stop()
            for b in buttons:b.configure(state='normal')
            entry.configure(state='normal');status.set(text)
            if not ok:messagebox.showerror('Operation stopped',text)
            elif len(text)>250:messagebox.showinfo('Finished',text)
        except queue.Empty:pass
        root.after(100,poll)
    def close():
        if busy:messagebox.showinfo('Operation in progress','Wait for the operation to finish before closing.')
        else:root.destroy()
    root.protocol('WM_DELETE_WINDOW',close)
    root.after(100,poll);root.mainloop()

if __name__=='__main__':main()
