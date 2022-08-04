// implement the server side of the local server
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net;
using System.Net.Sockets;

namespace Server {
    public class Program {
       private const int PORT = 10385;

        public static void Main(string[] args) {
            Socket server = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            IPEndPoint ep = new IPEndPoint(IPAddress.Any, PORT);
            server.Bind(ep);
            server.Listen(10);
            
            Socket socket = server.Accept();
            Console.WriteLine("Connected");

            // TODO: Implement the communication feature with python
        }
    }
}