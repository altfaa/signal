from kit.sql_api.get_df.volumer import get_df_all_volumes
from kit.plot.volume_day import good_make_table_volumes
from kit.telegram_api.send import send_photo_to_my_channel
from datetime import datetime, timedelta


date_str_param = str(datetime.now() - timedelta(days=1))[:10]
date_string_title = (datetime.now() - timedelta(days=1)).strftime("%d %b %Y %H:%M")

df = get_df_all_volumes(date_str_param)
out_filename = "123.png"
good_make_table_volumes(df=df, out_filename=out_filename, tittle=date_string_title)
photo_fp = open(out_filename, 'rb')
send_photo_to_my_channel(photo_fp=photo_fp, text_message="270223")
photo_fp.close()
