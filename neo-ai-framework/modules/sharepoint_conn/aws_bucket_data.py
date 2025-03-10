import os
import boto3
import tempfile
from office365.runtime.auth.client_credential import ClientCredential
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File


def s3_to_sharepoint(
        s3_bucket_name,
        s3_prefix,
        sharepoint_site_url,
        sharepoint_folder_path,
        client_id,
        client_secret
        ):

    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
        )

    # Inicializar o contexto do SharePoint
    credentials = ClientCredential(client_id, client_secret)
    ctx = ClientContext(sharepoint_site_url).with_credentials(credentials)

    # Listar objetos no bucket S3
    print(f"Listando objetos no bucket '{s3_bucket_name}' com prefixo '{s3_prefix}'...")
    paginator = s3_client.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=s3_bucket_name, Prefix=s3_prefix):
        if 'Contents' not in page:
            print("Nenhum objeto encontrado.")
            return

        for obj in page['Contents']:
            s3_key = obj['Key']
            file_name = os.path.basename(s3_key)

            # Ignorar pastas (objetos que terminam com /)
            if file_name == '':
                continue

            print(f"Transferindo arquivo: {s3_key}")

            # Baixar arquivo do S3 para um arquivo temporário
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                s3_client.download_fileobj(
                    Bucket=s3_bucket_name,
                    Key=s3_key,
                    Fileobj=temp_file
                    )
                temp_file_path = temp_file.name

            try:
                # Construir o caminho completo para o arquivo no SharePoint
                sharepoint_file_path = f"{sharepoint_folder_path}/{file_name}"

                # Ler o conteúdo do arquivo temporário
                with open(temp_file_path, 'rb') as file_content:
                    # Upload do arquivo para o SharePoint
                    target_folder = ctx.web.get_folder_by_server_relative_url(sharepoint_folder_path)
                    target_folder.upload_file(file_name, file_content.read()).execute_query()

                print(f"Arquivo '{file_name}' transferido com sucesso para '{sharepoint_file_path}'")

            finally:
                # Remover o arquivo temporário
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)

    print("Transferência concluída!")


if __name__ == "__main__":
    # Configurações
    S3_BUCKET_NAME =
    S3_PREFIX = "pasta/no/s3/"  # Opcional, deixe vazio para transferir todo o bucket

    SHAREPOINT_SITE_URL = ""
    SHAREPOINT_FOLDER_PATH = ""

    # Credenciais do SharePoint (use variáveis de ambiente ou outro método seguro)
    CLIENT_ID = os.environ.get("SHAREPOINT_CLIENT_ID")
    CLIENT_SECRET = os.environ.get("SHAREPOINT_CLIENT_SECRET")

    # Executar a transferência
    s3_to_sharepoint(
        s3_bucket_name=S3_BUCKET_NAME,
        s3_prefix=S3_PREFIX,
        sharepoint_site_url=SHAREPOINT_SITE_URL,
        sharepoint_folder_path=SHAREPOINT_FOLDER_PATH,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
        )