from kit.sql_api.get_df.volumer import get_df_all_volumes
from kit.plot.volume_day import good_make_table_volumes
from kit.telegram_api.send import send_photo_to_my_channel


date = '2023-02-27'
df = get_df_all_volumes(date)
out_filename = "123.png"
good_make_table_volumes(df=df, out_filename=out_filename, tittle=date)
photo_fp = open(out_filename, 'rb')
send_photo_to_my_channel(photo_fp=photo_fp, text_message="270223")
photo_fp.close()
