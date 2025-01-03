# Multi-Conversor
Software para conversão de diferentes tipos de arquivos

# Motivação
Trabalho com produção musical, e constantemente preciso efetuar a conversão de arquivos de áudio de wav para mp3 ou para outros formatos. Até então utilizava um software muito conhecido no mercado, principalmente para os mais antigos, entretanto, após algumas postagens em fóruns sobre o uso do processamento das máquinas para mineração de forma anônima por parte dos desenvolvedores, e observações próprias de comportamentos anormais do software, causando lentidão e até travamentos no meu computador decidi por desinstalar o software e passei a utilizar sites para este fim, que também não era a solução ideal, uma vez que havia arquivos de vídeo com vários gigas de tamanho, tornando inviável o upload e o download. Então, decidi criar meu próprio conversor de arquivos.

Na tela inicial, temos os tipos de arquivos a converter, Audio, vídeo e imagem. 

![image](https://github.com/user-attachments/assets/2ef72b2d-0c47-49fe-9d64-48492116875d)

A conversão de Audio converte arquivos entre as extensões: MP3, WAV, FLAC, OGG E AAC. O usuário clica em selecionar arquivo, em seguida, define para qual extensão o áudio será convertido e clica em start.

![image](https://github.com/user-attachments/assets/31c6ba27-83a9-408b-9f87-af8dc8d940c0)

A barra de progesso sinalizará o progresso e um aviso será exibido. O arquivo convertido estará na mesma pasta que o arquivo original.

Igualmente, a Conversão de Vídeo, converte os arquivos entre as extensões: MP4, AVI, MOV, MKV, FLV e também para MP3, que não é uma extensão de vídeo, mas é útil para aqueles que quiserem converter um vídeo em áudio. Com o mesmo visual da conversão de áudio, também terá uma barra de progresso indicando o status da conversão. E assim como a conversão de áudio, o arquivo aqui também fica salvo no mesmo local que o arquivo original.

Da mesma forma, a Conversão de Imagem, converte os arquivos entre as extensões: JPG, PNG, BMP, GIF e ICO. Esse é interessante, pois para deixar o software com ícone, precisava criar arquivos .ico, então, após criar a imagem, utilizava um site para essa conversão, e foi neste software onde a ideia de conversão começou. Se eu consegui criar um software que converte png para ico, por que não consigo para outras extensões? E melhor, por que não consigo para outros tipos de arquivos? Inclusive, todos os ícones do visual do software, estão em png, e ico, todos convertidos pelo código inicial do Multi Conversor ainda em python, na fase de testes.

O Software ainda conta com um botão de doação, para auqeles que quiserem ajudar meu trabalho e ajudar a custear a faculdade. O software será disponibilizado gratuitamente na internet, assim com alguns outros projetos que estou montando, e que ficarão disponíveis no meu site - https://aplicacoessimples.blogspot.com/

# DESENVOLVIMENTO E COMPILAÇÃO

Alguns desafios tiveram de ser superados durante o desenvolvimento, como a inclusão das imagens para tornar o software mais intuitivo e visualmente agradável, pois na versão inical era tudo apenas texto. Para o uso de imagens, precisei embutir as imagens dentro do exe. Para a conversão de py para exe, utilizo o auto_py_to_exe, mas para que as imagens possam funcionar, foi necessário criar um arquivo .qrc mapeando as imagens, e no código python, alterar a linha iconpath (que é a variável que utilizo para as imagens no código), neste ponto, precisei contar com a ajuda da inteligência artificial, pois era um conhecimento que ainda não havia adquirido nos estudos que tenho feito.
A opção era criar um arquivo compactado, onde o usuário precisaria descompactar numa pasta, neste arquivo, teria a pasta img onde ficam as imagens, mas caso o usuário fizesse errado, ou excluísse, ou não descompactasse a pasta img, o software abriria sem nenhum dos ícones, então a opção mais viável foi embutir as imagens dentro do executável. Após a criação do arquivo qrc, realizei a compilação do mesmo pelo comando no terminal python PyQt5.pyrcc_main resources.qrc -o resources_rc.py (necessário ter a biblioteca PyQT5-Tools instalado) e adicionar a biblioteca resources_rc no código (import resources_rc). Feito isso, foi iniciada a fase de testes, executando o software ainda no script, testando as funções, tudo funcionando perfeitamente. Em seguida, foi hora de compilar para exe, e testar as funções. Ainda encontrei alguns problemas, mas foram aos poucos sendo solucionados, e agora o software é 100% funcional.

Nessa versão é possível converter apenas um arquivo por vez. Em breve estarei aplicando melhorias para conversão múltipla de arquivos.
