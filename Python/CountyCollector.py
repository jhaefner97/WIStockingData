import openai
from db import Database
from Models.WIStockingData import WIStockingData
from utils import logger, Constants, Utilities, Paths

paths = Paths()

class App:
    def __init__(self):
        self.DB = Database()
        self.DB.test_connection()  # Test the connection on initialization
        self.session = self.DB.create_session()

    def get_database_results(self) -> list[WIStockingData]:
        return self.session.query(WIStockingData).filter(WIStockingData.County == None).all()
    
    def get_processed_counties(self) -> list[WIStockingData]:
        return self.session.query(WIStockingData).filter(WIStockingData.County != "").all()
    
    def build_processed_county_dictionary(self) -> dict[str, str]:
        processed_data = {}
        processed_rows = self.get_processed_counties()
        for obj in processed_rows:
            processed_data[obj.StockedWaterbodyName] = obj.County
        return processed_data
    
    def open_ai_query(self, system_prompt: str, user_prompt: str, model: str = "gpt-3.5-turbo-0125", max_tokens: int = 100) -> str:
        """
        Generates a response from the OpenAI API based on the input prompt.
        
        Args:
            prompt (str): The input text prompt to provide to the model.
            model (str): The OpenAI model to use (default: 'gpt-4').
            max_tokens (int): The maximum number of tokens in the output.
            
        Returns:
            str: The generated response from the model.
        """
        openai.api_key = Constants.OPENAI_API_KEY
        try:
            response = openai.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=max_tokens,
                temperature=0.3,  # Adjust for creativity (0.0 is deterministic, 1.0 is very creative)
            )
            
            # Extract the response text
            return response.choices[0].message.content.strip("[]\"")
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            raise e

    def main(self):
        try:
            processed_data = self.build_processed_county_dictionary()
            results = self.get_database_results()
            counter = 0
            sys_prompt = Utilities.read_text_file(paths.county_lookup_prompt_file)
            for result in results:
                if result.StockedWaterbodyName in processed_data.keys():
                    result.County = processed_data.get(result.StockedWaterbodyName, None)
                else:
                    result.County = self.open_ai_query(system_prompt=sys_prompt, user_prompt=result.__repr__())
                    processed_data[result.StockedWaterbodyName] = result.County
                counter+=1
                if counter == 1000: #  Commit in batches
                    self.session.commit()
                    logger.info("Committed Batch")
                    counter = 0
            self.session.commit()
        except Exception as e:
            logger.error(f"Query failed: {e}")
            raise e

if __name__ == "__main__":
    app = App()
    app.main()