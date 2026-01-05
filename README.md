Software de alta performance para conversão em massa de arquivos multimídia. Projetado com uma interface moderna e intuitiva, permite processar múltiplos arquivos simultaneamente sem travar a interface.
🛠 Recursos
Imagens: Conversão entre JPG, PNG, BMP e ICO.
Áudio: Conversão de alta fidelidade entre MP3, WAV, FLAC e OGG.
Vídeo: Conversão de formatos MP4, AVI, MOV e MKV.
Extração de Áudio: Converta vídeos diretamente para MP3 com um clique.
Processamento em Lote: Selecione dezenas de arquivos e o software cuidará do resto.
⚙️ Requisitos de Instalação (FFmpeg)
O software utiliza o motor FFmpeg para o processamento de vídeo e áudio.
Baixe o FFmpeg em ffmpeg.org.
Extraia os arquivos (recomendado: C:\ffmpeg).
Adicione a pasta bin às Variáveis de Ambiente do Windows:
No Menu Iniciar, digite "Variáveis de ambiente" e abra a opção correspondente.
Clique em Variáveis de Ambiente.
Em Variáveis de Sistema, localize a variável Path e clique em Editar.
Clique em Novo e cole o caminho: C:\ffmpeg\bin.
Dê OK em todas as janelas.
🚀 Como Utilizar
Inicie o aplicativo e digite seu nome para personalização.
Escolha o módulo desejado (Áudio, Vídeo ou Imagem).
Clique em Selecionar Arquivos e escolha quantos desejar.
Escolha o formato de saída e clique em Iniciar Conversão.
Os arquivos convertidos serão salvos na mesma pasta dos originais com o sufixo _convertido.
💻 Tecnologias Utilizadas
Interface Gráfica: PyQt5 (Layout moderno e responsivo).
Estilização: QSS (Qt Style Sheets) para Design Dark Mode.
Motor de Áudio/Vídeo: Pydub + FFmpeg.
Motor de Imagem: Pillow (PIL).
Automação: urllib para gestão de componentes.