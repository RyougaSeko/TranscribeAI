import os
import os.path
import dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)

DeepL_API_KEY = os.environ.get("DeepL_API_KEY")