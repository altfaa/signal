from kit.sql_api.get_df.volumer import get_df_all_volumes
from kit.plot.volume_day import good_make_table_volumes
from kit.telegram_api.send import send_photo_to_my_channel
from datetime import datetime, timedelta
from kit.names.channel import CHANNEL_NAME

date_str_param = str(datetime.now() - timedelta(days=1))[:10]
date_string_title = (datetime.now() - timedelta(days=1)).strftime("%d %b %Y")

df, info_list = get_df_all_volumes(date_str_param)

name = info_list[0]
vol = info_list[1]
cost = info_list[2]
total = info_list[3]

#cost_string = f"{cost:,}".replace(',', ' ')
total_string = f"{total / 1000000000:.1f}"

text = f"Дневной оборот\n\n🗓 {date_string_title}\n\n __Σ__  {total_string} млрд.₽\n\n" + f"{CHANNEL_NAME}".replace("_",
                                                                                                                  "\\_")

out_filename = "volume_hbar.png"
good_make_table_volumes(df=df, out_filename=out_filename, tittle=date_string_title, info=[name,vol,cost])
photo_fp = open(out_filename, 'rb')
send_photo_to_my_channel(photo_fp=photo_fp, text_message=text)
photo_fp.close()
