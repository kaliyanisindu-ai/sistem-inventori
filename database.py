import mysql.connector


db = mysql.connector.connect(

    host="gateway01.ap-southeast-1.prod.alicloud.tidbcloud.com",
    user="4Mb7mMDdCgpgEcr.root",
    password="kdfNjfK8kxwAqoMo",
    database="sistem_inventori",
    port=4000

)


print("Database berhasil terhubung")