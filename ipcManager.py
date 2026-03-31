import sysv_ipc

class ipcManager:
    def __init__(self, key=1234):
        self.key = key
        self.mq = None

    def connectCreate(self):
        # ma conectez la coada existenta sau creez coada noua
        try:
            self.mq = sysv_ipc.MessageQueue(self.key, sysv_ipc.IPC_CREAT, 0o666)
            print(f"Connected to {self.key}")
            return True
        except sysv_ipc.Error as e:
            print(f"Eroare IPC: {e}")
            return False

    def sendMessage(self, message_str, msg_type = 1):
        if self.mq:
            self.mq.send(message_str.encode('utf-8'), type=msg_type)
            print(f"Trimis tip {msg_type}: {message_str}")

    def receiveMessage(self, msg_type = 0):
        if self.mq:
            try:
                mesaj_bytes, t = self.mq.receive(block=False, type=msg_type)
                mesaj_decodat = mesaj_bytes.decode('utf-8')
                print(f"Primit tip {msg_type}: {mesaj_decodat}")
                return mesaj_decodat
            except sysv_ipc.BusyError:
                return None
            except sysv_ipc.ExistentialError:
                return None
        return None

    def destroyQueue(self):
        if self.mq:
            try:
                self.mq.remove()
                print("Coada ipc a fost stearsa")
            except sysv_ipc.ExistentialError:
                pass

