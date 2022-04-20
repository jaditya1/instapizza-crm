from UserRole.models import DownloadToken
import secrets




def token_create():
	token_data = {}
	auth_token = secrets.token_hex(48)
	create_record = DownloadToken.objects.create(auth_token=auth_token)
	row_id = create_record.id
	token_data["download_token"] = auth_token
	token_data["token_id"] = row_id
	return token_data


def token_delete(row_id):
	delete_record = DownloadToken.objects.filter(id=row_id).delete()
	return True
