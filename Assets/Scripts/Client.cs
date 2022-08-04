using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net;
using System.Net.Sockets;

using UnityEngine;

public class Client : MonoBehaviour {
    private const int PORT = 10385;
    Socket socket;

    void Start() {
        Debug.Log("Client started");
 
        // Creation TCP/IP Socket using
        // Socket Class Constructor
        socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        socket.Connect("127.0.0.1", PORT);
        Debug.Log("Connected");
    }

    void Update() {
        // TODO: Implement the communication feature with python
        try {
            byte[] data = new byte[socket.Available]; 
            int length = socket.Receive(data, data.Length, SocketFlags.None);
            Array.Reverse(data);
            Debug.Log(Encoding.UTF8.GetString(data));
        } catch {

        }
    }
}