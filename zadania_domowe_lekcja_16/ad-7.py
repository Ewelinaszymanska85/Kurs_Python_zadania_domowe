def parse_url(url: str) -> dict:
    """
    Parsuje adres URL i zwraca slownik z jego skladowymi:
    protocol, domain, port, path.

    Przyklad:
        parse_url("https://api.example.com:8080/users/search?active=true")
        -> {'protocol': 'https', 'domain': 'api.example.com', 'port': 8080,
            'path': '/users/search?active=true'}
    """
    try:
        # 1. Wyciagnij protokol
        protocol, reszta = url.split("://")

        # 2. Wyciagnij sciezke
        if "/" in reszta:
            host, path = reszta.split("/", 1)
            path = "/" + path
        else:
            host = reszta
            path = "/"

        # 3. Sprawdz czy jest port
        if ":" in host:
            domain, port = host.split(":")
            port = int(port)
        else:
            domain = host
            port = 80 if protocol == "http" else 443

        return {
            "protocol": protocol,
            "domain": domain,
            "port": port,
            "path": path
        }

    except ValueError as e:
        print(f"Blad podczas parsowania URL '{url}': {e}")
        return {}


if __name__ == "__main__":
    testowe_url = [
        "https://api.example.com:8080/users/search?active=true",
        "http://example.com/index.html",
        "https://google.com",
    ]

    for url in testowe_url:
        wynik = parse_url(url)
        print(f"URL: {url}")
        print(f"  -> {wynik}\n") 