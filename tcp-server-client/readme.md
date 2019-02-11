This small project is the interaction of a client (clients) and a server via tcp sockets. The server accepts various metrics of imaginary loads of other servers for further analysis and also gives the necessary metrics upon request. There are messaging format agreements between the server and clients, which streamlines and simplifies communication. 

The format for sending data by the client is "put palm.cpu 10.6 1501864247\n", where the first is the sending command, the second is the name of the metric, the third is the value of the metric and the fourth is the unix timestamp.

The format for receiving the metric is "get palm.cpu\n", where the first is the receiving command, and the second is the name of the metric (instead of the name it can be "*", then the server should return all available metrics.

The server can respond as follows: 
1) "ok\n\n" - to add a metric is a successful execution, and to get it, everything worked out correctly, but there is no such metric on the server
2) "ok\npalm.cpu 10.5 1501864247\neardrum.cpu 15.3 1501864259\n\n" - when the server gives the necessary metrics and everything worked correctly
3) "error\nwrong command\n\n "- incorrect request from the client.
The end of the server message always has two newline characters.
