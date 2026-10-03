import {spawn} from 'node:child_process';
import {join} from 'node:path';
const python=process.env.CHURCH_PYTHON || join('.venv',process.platform==='win32'?'Scripts':'bin',process.platform==='win32'?'python.exe':'python');
const proc=spawn(python,['iniciar.py'],{stdio:'inherit'});
proc.on('error',()=>{console.error('Instale o ambiente Python conforme LEIA-ME-WINDOWS.md.');process.exit(1)});
proc.on('exit',code=>process.exit(code||0));
