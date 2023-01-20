import pymongo

koneksi_url = "mongodb://localhost:27017/"

def createDatabase(url_client, database, collection, document):
    myclient = pymongo.MongoClient(url_client)
    mydatabase = myclient[database]
    mycollection = mydatabase[collection]
    mydocument = mycollection.insert_one(document)

    return mydocument


class MongoAPI:
    def __init__(self, data, url_client):
        self.client = pymongo.MongoClient(url_client)

        database = data['database']
        collection = data['collection']
        cursor = self.client[database]
        self.collection= cursor[collection]
        self.data = data

    def read(self):
        documents = self.collection.find()
        value = [{
            item: data[item] for item in data if item != '_id'} for data in documents]
        return value


    def create(self, data):
        new_document = data['document']
        response = self.collection.insert_one(new_document)
        value = {
            'status' : 'berhasil',
            'document_id' : str(response.inserted_id)
        }
        return value


    def update(self):

        filt = self.data['filter']
        update_data = {
            "$set": self.data['dataUpdate']
        }
        response = self.collection.update_one(filt, update_data)
        value = {
            "status": "berhasil diupdate" if response.modified_count > 0 else "tidak ada data yang perlu diupdate"
        }
        return value

    def delete(self, data):
        filt = data['document']
        response = self.collection.delete_one(filt)
        value = {
            'status': 'berhasil dihapus' if response.deleted_count > 0 else "document tidak ditemukan"
        }
        return value

if __name__ == '__main__':
    data = {
        "database": "DBperusahaan",
        "collection": "pegawai",
        "filter": {
            'name': "Ahmad Fauzan"
        },
        'dataUpdate' : {
            'name' : "RRQ Lemon"
        }
    }

    # namadb = 'DBperusahaan'
    # namacol = 'pegawai'
    # documents = { 'name': 'Ahmad Fauzan' }      
    # buat_db = createDatabase(koneksi_url, namadb, namacol, documents)

    mongo_objek = MongoAPI(data, koneksi_url)
    mongo_objek.update()
    mongo_objek.create({
        'document': {
            'name' : 'Faiz'
        }
    })          