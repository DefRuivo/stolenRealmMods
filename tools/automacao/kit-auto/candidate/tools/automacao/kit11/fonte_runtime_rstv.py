"""Fonte LIVE somente-leitura para executor KIT11; nunca navega nem emite comandos.
Arquivo e transporte, nao replay: exige processo vivo esperado, sessao/motor/hash pinados,
heartbeat UTC fresco e avanco de frame observado DURANTE a consulta desta instancia.
O chamador fornece pid_vivo real (na bancada: Get-Process com caminho do exe).
"""
import json
import math
from pathlib import Path
import time

SCHEMA = 'KIT-RSTV-INT/runtime/1'

class FonteRuntimeRSTV:
    def __init__(self, caminho, *, pid, sessao, motor, adapter_sha256, pid_vivo,
                 idade_max_s=3.0, relogio_utc=time.time):
        if type(pid) is not int or pid <= 0 or not callable(pid_vivo):
            raise ValueError('PID esperado e verificador real obrigatorios')
        if any(not isinstance(v, str) or not v for v in (sessao, motor, adapter_sha256)):
            raise ValueError('identidade esperada obrigatoria')
        if type(idade_max_s) not in (float,int) or not math.isfinite(idade_max_s) or idade_max_s <= 0:
            raise ValueError('idade maxima finita positiva obrigatoria')
        self.caminho=Path(caminho); self.pid=pid; self.sessao=sessao; self.motor=motor
        self.sha=adapter_sha256; self.vivo=pid_vivo; self.max_age=idade_max_s; self.now=relogio_utc
        self.frames=[]; self.amostras=[]; self._primeiro=None; self._ultimo=None

    @property
    def runtime_exercitado(self):
        return len(set(self.frames)) >= 2

    def ler(self, tipo, alvo):
        def no(why): return {'satisfeito':False,'observado':None,'diagnostico':why}
        if self.vivo(self.pid) is not True: return no('PID esperado nao vivo/mensuravel')
        try:
            d=json.loads(self.caminho.read_text(encoding='utf-8-sig'))
        except (OSError,ValueError): return no('heartbeat ausente/ilegivel')
        if not isinstance(d,dict): return no('heartbeat nao e objeto')
        e=d.get('engine')
        if not isinstance(e,dict): return no('engine ausente')
        if d.get('esquema')!=SCHEMA or d.get('ativo') is not True or d.get('erro_contexto') is not None:
            return no('schema/inatividade/erro de contexto')
        if (e.get('pid'),e.get('sessao'),e.get('motor_id'),e.get('adapter_sha256')) != (self.pid,self.sessao,self.motor,self.sha):
            return no('identidade live divergente')
        utc=e.get('utc_unix_ms');frame=e.get('frame')
        if type(utc) is not int or type(frame) is not int or frame<0: return no('relogio/frame invalidos')
        age=self.now()-utc/1000
        if age < -0.5 or age > self.max_age: return no('heartbeat vencido/futuro')
        if self._ultimo is not None and frame<self._ultimo: return no('frame regrediu')
        self._ultimo=frame
        if self._primeiro is None: self._primeiro=frame
        self.frames.append(frame)
        self.amostras.append({'engine':e,'tipo':tipo,'alvo':alvo,'idade_s':age,'janelas_ativas':d.get('janelas_ativas')})
        if len(self.amostras)>100: self.amostras.pop(0)
        if frame<=self._primeiro: return no('aguardando avanco de frame vivo')
        if tipo=='condicao' and alvo in ('jogo_aberto','probe_carregado'):
            ok=True
        elif tipo=='tela':
            windows=d.get('janelas_ativas')
            ok=isinstance(windows,list) and alvo in windows
        else:
            return no('alvo nao suportado pela fonte live RSTV')
        return {'satisfeito':ok,'observado':{'engine':e,'janelas_ativas':d.get('janelas_ativas')},
                'diagnostico':'engine viva com frame crescente' if ok else 'janela nao observada na engine viva'}
