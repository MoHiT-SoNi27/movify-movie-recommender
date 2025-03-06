import dropbox
from dropbox.files import WriteMode
import os
ACCESS_TOKEN = "sl.u.AFlQndNLiCnWhBBsgr1eQAeIYWwGUVBKtQOz7A9CntomsVDaiSCwtLapt6ByAxnpm4sYnDc6wc3j6UeucpYEI269bu9hANn4a1e0JBYclgZ2RRH1woecR4I2NGRaUcJS4i2wRHT8DCwYXK8xI_5RKHAflJAPxFvDMy_EIHv7habSxAxUCn7yEcQQhBwiYA90kI_yLSaYGczPWsD7tFPrrFPEy1aZnn0Jgc-6QkE6KNDWiFOT6YI7wJ4_FsRxuZ8AjKH3Xef9huX5yO4Ny09muV9Euj2nE4Gq7p4nBDJ5ASzm6kSawVdQy2QGuj-yHi9f1XKg5c1hhJrh0gLu_Gmjr6Qi78p1FdyoBGUe4TWB4HjkBd--1PyU1dgLNcW9wPNZ8G_jigs6f0xbeR3LCxjDx476toAQcJwoKMaytZ8Z6JGydBL3ouzFuUqmLrLLtYj3_GCdekdb3Naa__35bkDWJCCam-tqOQCZ69AXshAUsGg2H8dpr2pzaTIgYrsVMoxDPRQh6thgHaGFeOyXat_qtb1d0szel6fpA3Fy35wHS4rtXuT6FYw7t12hUaYJTT9RGDEiYPFDs9KZ1Xqffx8TS6uIHynhK5xCFFU5pDrjKeyjQmqew9_FvNQTa6Yowqg7g44xlaRC55OweD6yAKBAStC8nG0nGHH-fcG8FL_siZsKnI38O4ud6FyFVAjfXjqKEfZ6bBFaRCOfu0BbQSf1qBHVLf7sQ7DNdDLRvD5AGHtiU-7KaTM8uCZEEfwnmviECWbs7qcCIhv7jlEJaiHyTL1wDNMp6tEgZu5Lx_nlm5rRFl6R8XZqDX50kzBWqrwfIjLTPhszdc_nDvHIvIrmhv_hQeMMvPolRw9tbBcp6mTR1FXgg002xI4c6MhVQB-k8Fp5LIVRf1yFhKy9KOmzWGC7zN9bqxOkVA5pD9erO0dnhxJkYVwgWNEXHrCkpkxwnM5zl5QPIm5TEJbU_ObUEgA5brU8z26g9SvHOwfJsOeToQiTboIt01jc0HEY6pvPMlGYkgj1q8AxRZHXtX3oc3ECS_c84E2dr4dwRDvRZz9T728NMsOntqrRv6to6XG2PuqagSJaCUlVCnXcD56bW0qilHAoeNSO-I3Lud7Z2N_lUtizo0MxCirk6WlNwf6S3zEzc_iByAPhWhnot1zCQ8TSz9dnTKLAWUJ5MCKU6bnXAxdX825XcaLtTL3YpiBhCapebSZ53LD_MKht78dvMQSuHa07Do2YoOcRTtyhUz8X8rsOzfAP6WGaI-hQbv2tjzokJX-qq_A0Le9b8wfFlXBIfMAPLo7okUgGHHg_jRlTNhLGoffcK4CayDn7_gYTP0qSJDCSMbmiQUVKqSime-tWeen-UovzAGqrCpl2UhwNna790cRd9Y-iYpnZAkf_vjGl_gjW3hY2x_vEII0ebNmm"
# Upload files to Dropbox
def upload_large_file(local_file, dropbox_path):
    dbx = dropbox.Dropbox(ACCESS_TOKEN)

    chunk_size = 4 * 1024 * 1024  # 4MB chunks
    file_size = os.path.getsize(local_file)

    with open(local_file, "rb") as f:
        session_start_result = dbx.files_upload_session_start(f.read(chunk_size))
        cursor = dropbox.files.UploadSessionCursor(session_start_result.session_id, offset=f.tell())
        commit = dropbox.files.CommitInfo(path=dropbox_path)

        while f.tell() < file_size:
            if (file_size - f.tell()) <= chunk_size:
                dbx.files_upload_session_finish(f.read(chunk_size), cursor, commit)
            else:
                dbx.files_upload_session_append_v2(f.read(chunk_size), cursor)
                cursor.offset = f.tell()

upload_large_file(r"C:\WEBDEV\Movie Recommender\movie_dict.pkl", "/movie_dict.pkl")
upload_large_file(r"C:\WEBDEV\Movie Recommender\movies.pkl", "/movies.pkl")
upload_large_file(r"C:\WEBDEV\Movie Recommender\similarity.pkl", "/similarity.pkl")

