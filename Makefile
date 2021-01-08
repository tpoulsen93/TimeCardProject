default: getPhone.c
	gcc -o getPhone getPhone.c -g -Wall

java: TimeCard.java GenerateTimeCards.java
	javac TimeCard.java GenerateTimeCards.java

clean:
	rm -fr *.class getPhone
