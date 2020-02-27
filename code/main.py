import pandas as pd
import hashlib

def main():
    files = ['00.csv', '01.csv', '02.csv', '03.csv', '04.csv', '05.csv', '06.csv', '07.csv', '08.csv', '09.csv', '10.csv', '11.csv', '12.csv', '13.csv', '14.csv']
    for x in files:
        event_raw = pd.read_csv('raw_data/events/'+x,
                                  header=None,
                                  names=['imsi','imei','cell_id','tac','rac','sac','area_id',
                                         'segment','ts_start','ts_end','erm','trf'])

        #get columns of interest
        event = event_raw[['imsi','cell_id','area_id','ts_start','ts_end']]

        #drop duplicates
        event_unique = event.drop_duplicates(keep='first')

        cell = pd.read_csv('raw_data/de_cells.csv')

        #rename columns on the cell dataframe to later on make an inner joint with the event dataframe
        cell_renamed = cell.rename(columns={'cid':'cell_id','area':'area_id'})

        #remove duplicates before inner join
        event_no2 = event_unique.drop_duplicates(subset=['cell_id','area_id'])
        cell_no2 = cell_renamed.drop_duplicates(subset=['cell_id','area_id'])

        #inner join with the cell dataframe to atribute coordinates to signals
        df_merged = event_no2.merge(cell_no2, on=['cell_id','area_id'], how='inner')

        def sha256(i):
            s=str(i)
            converted = hashlib.sha256(s.encode())
            return converted.hexdigest()

        df_merged['imsi_sha256'] = df_merged['imsi'].apply(sha256)

        df_private = df_merged.drop(columns=['imsi'])

        df_interest =df_private.loc[(df_private['imsi_sha256']=='ce9e62301ddce626128b708220d2498d34c38f0ceac753de4836b426a0747a29')
                                   |(df_private['imsi_sha256']=='0df96b53e1bd1b4cd1377ce2dcf7f12bb9384f915e2f12d1bbc4e5e5b2668b90')
                                   |(df_private['imsi_sha256']=='7a3751d3534bd8e50e69afc6a1d3e40b5d14fc33b12333dc7649a05ad224971c')
                                   |(df_private['imsi_sha256']=='149394f92c7b6e07d66c792a68b0f232064fe9eff5d873da1486e81280592a48')]

        df_sorted = df_interest.sort_values(by=['ts_start']) #to draw movement chains chronologically

        df_sorted.to_csv('events_treated/'+x)

if __name__=='__main__': #entry point for my program
    main()
