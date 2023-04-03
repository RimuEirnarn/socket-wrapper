# Socket Wrapper

This is a random socket wrapper that is mostly written by ChatGPT but refined. You can subclass the `Server` and `Client` classes for your needs.

## Basic information

Both server and client use socket, with `AF_INET` and `SOCK_STREAM`.

Both classes use selectors to handle read events.

Both classes should be capable of reading a large amount of data but data safety is **NOT** guaranteed.

Client and Server use threading to help stuff not go in the main thread's way (usually, they block when reading a lot of chunks).

For the Client class, the `block_read` function will "block" until the data is received successfully.

## Changelogs

No changelogs. Lmao.

## License

This repo uses the MIT license. Feel free to use it.