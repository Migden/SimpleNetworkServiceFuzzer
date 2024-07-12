import socket
import argparse
import time

class ConnectionHandler():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.EstablishConnection()

    def EstablishConnection(self):
        try:
            self.Connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except:
            print("Esablishing Socket Communication failed")
            quit()
        try:
            self.Connection.connect((self.ip, self.port))
        except:
            print("Error when Establishing Connection to remote service")
            quit()
        ## print(f"Established Connection With Server {self.ip}:{self.port}")
        return

    def SendInformation(self, Information):
        self.Connection.send(Information)
        return

    def RecoverInformation(self):
        data = self.Connection.recv(1024)
        return data

    def close(self):
        self.Connection.close()
        return

def payload(Index):
    ## Add Custom Fuzzing payloads and configuration here
    return 'A' * Index

def Fuzzing(ExpectedOutput, FuzzingRange, FuzzingPort, FuzzingIP):
    for i in range(1, FuzzingRange):
        Connection = ConnectionHandler(FuzzingIP, FuzzingPort)
        time.sleep(0.1)
        InputData = payload(Index=i)
        trash = Connection.RecoverInformation()
        Connection.SendInformation(InputData.encode('utf-8'))
        data = Connection.RecoverInformation()
        if data == ExpectedOutput:
            print(f"{InputData} - {data}")
            del Connection
            trash = ''
            continue
        else:
            print(f"Fuzzing Detected A Difference in results on index {i}: {data}")
            quit()


def DetermineExpectedOutput(EstablishedConnection):
    trash = EstablishedConnection.RecoverInformation()
    EstablishedConnection.SendInformation("Hello World".encode('utf-8'))
    Result = EstablishedConnection.RecoverInformation()
    if Result:
        print(f"Esablished Expected Output : {Result}")
        print("Continuing Fuzzing Startup")
    else:
        print(f"Expected Output Not Able to Be Established")
    
    EstablishedConnection.close()
    return Result

def CustomFuzzingParameters(EstablishedConnection, Port, IP):
    CustomFuzzingRange = 10000
    Result = DetermineExpectedOutput(EstablishedConnection=EstablishedConnection)
    Fuzzing(ExpectedOutput=Result, FuzzingRange=CustomFuzzingRange, FuzzingPort=Port, FuzzingIP=IP)

def main(args):
    EstablishedConnection = ConnectionHandler(args.host, args.port)
    CustomFuzzingParameters(EstablishedConnection=EstablishedConnection, Port=args.port, IP=args.host)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    ## parser.add_argument('-h', "--help", required=False)
    parser.add_argument('-p', "--port", type=int, required=True)
    parser.add_argument('-i', "--host", type=str, required=True)
    args = parser.parse_args()
    '''if args.help:
        print("""
              
 Option: -h, --help / Displays Help Information
 Option: -p, --port / Port Number For program to establish Connection
 Option: -i, --host / Host IP address for program to establish Connection

        """)
        quit()'''
    main(args)
