# Exercicio3_CE
Bibliotecas necessárias para execução do projeto:
```bash
pip install grpcio
pip install grpcio-tools
pip install pandas
pip install numpy
pip install regex
```

Para executar os programas é necessário ter o ip onde o servidor será alojado.
Com isso em mãos, no arquivo src\cade_analytics\cade_analytics_server.py, substitua server address pelo ip do servidor.

Para executar o servidor, execute o comando abaixo:
```bash
python src\cade_analytics\cade_analytics_server.py
```

Para executar o cliente, execute o comando abaixo (em outro terminal):
```bash
python src\cade_analytics\cade_analytics_client.py
```