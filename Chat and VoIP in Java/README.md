# Chat and VoIP Application

## Introduction
This project is a simple Peer-to-Peer (P2P) application that enables real-time chat and Voice over IP (VoIP) communication utilizing the UDP protocol in Java. This application will be based on java.net to handle network communications, providing a foundational understanding of network programming, concurrency, and instant messaging and multimedia data exchange between two peers.It is developed as part of the **Computer Networks II** course in the 7th semester of my studies and enables two users to communicate through text messages and voice calls without relying on a central server, ensuring end-to-end encrypted communication.

## Features
- **Text Messaging**: Users can send and receive encrypted text messages.
- **Voice Communication**: Real-time VoIP calls using UDP sockets.
- **End-to-End Encryption**: AES encryption secures text messages during transmission.
- **Decentralized Communication**: No central server is required.
- **Graphical User Interface**: Built using Java Swing for an intuitive user experience.
- **Multithreading**: Ensures simultaneous handling of text and voice communication.

## Technologies Used
- **Java** (Networking, Swing GUI, Cryptography)
- **UDP Sockets** (For real-time communication)
- **AES Encryption** (For securing messages)
- **Multithreading** (For handling multiple tasks simultaneously)

## How It Works
1. **Setup**: Both users must know each other's IP addresses and predefined port numbers.
2. **Messaging**: Text messages are encrypted using AES and transmitted over UDP.
3. **Voice Calls**: Audio is captured, transmitted, and played back in real-time.
4. **No Central Server**: All communication is direct between users.

## Installation and Usage
1. Clone the repository:
   ```sh
   git clone https://github.com/geotsad/Chat-VoIP.git
   cd Chat-VoIP
   ```
2. Compile the Java source files:
   ```sh
   javac -d bin src/com/cn2/communication/*.java
   ```
3. Run the application:
   ```sh
   java -cp bin com.cn2.communication.App
   ```
4. Enter the remote IP address and start chatting or making calls.

## Notes
- Ensure both users have the correct ports open.
- UDP is used for minimal latency, but may not guarantee delivery.
- The default encryption key should be changed for security purposes.

## Future Improvements
- Support for additional encryption methods.
- Improved GUI for better user experience.
- Enhanced audio quality with different codecs.

## License
This project is for educational purposes and follows an open-source license.

## Contact

* Name: Georgios Tsantikis
* Email: giotsa44@gmail.com
* GitHub: geotsad

[Return to the top](#matrices-and-vector-operations-in-c)

