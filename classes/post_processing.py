import os
import pandas as pd # type: ignore

class PostProcessing:
    def __init__(self, sim_path: str, filename: str):
        self.sim_path = sim_path
        self.filename = filename
        self.filepath = os.path.join(sim_path, filename)

    def process(self) -> pd.DataFrame:
        try:
            df = pd.read_csv(self.filepath)
        except Exception as e:
            raise IOError(f"Erro ao ler o arquivo CSV: {e}")

        required_columns = ['EXNAME', 'HDAT', 'SDAT', 'PDAT', 'HWAM']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"As colunas a seguir estão ausentes no arquivo: {missing_columns}")

        df_filtered = df[required_columns].copy()

        # Convert SDATE e PDAT for integer
        df_filtered['SDAT'] = pd.to_numeric(df_filtered['SDAT'], errors='coerce').fillna(0).astype(int)
        df_filtered['PDAT'] = pd.to_numeric(df_filtered['PDAT'], errors='coerce').fillna(0).astype(int)

        # Apply the logic: if PDAT - SDAT < 15 → 0 for bouth
        for idx, row in df_filtered.iterrows():
            diff = row['PDAT'] - row['SDAT']
            #Caso a difença do plantio a emergência seja maior do que 12 ele zera
            #Case the diference between planting and emergece is big to 12, put the value 0
            if diff > 12:
                #df_filtered.at[idx, 'PDAT'] = 0
                #df_filtered.at[idx, 'EDAT'] = 0
                df_filtered.at[idx, 'HWAM'] = 0

        return df_filtered

    def save_processed(self, output_filename: str = '../processed_output.csv') -> None:
        df_processed = self.process()
        output_path = os.path.join(self.sim_path, output_filename)
        df_processed.to_csv(output_path, index=False)
        #print(f"[INFO] Post-processing done!\n")
