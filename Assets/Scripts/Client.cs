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

    void Start() {
        Debug.Log("Client started");
 
        // Creation TCP/IP Socket using
        // Socket Class Constructor
        Socket sender = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        sender.Connect("127.0.0.1", PORT);
        Debug.Log("Connected");

        // TODO: Implement the communication feature with python
        
    }
}