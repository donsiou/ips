import serial


ser=serial.Serial ('com7',9600)
while True:

    try:
        X=ser.readline()
        tmp = [X[i] for i in range(5)]
        print(tmp)
    except Exception:
        
