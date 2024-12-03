from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils import Constants, logger, Paths

paths = Paths()

class Database:
    def __init__(self):
        try:
            # Get the database URI from constants
            self.DATABASE_URI = Constants.DB_URI
            
            # SSL Configuration
            connect_args = {}
            if "mysql+pymysql" in self.DATABASE_URI:
                connect_args = {
                    "ssl": {
                        "ca": paths.ca_certificate  
                    }
                }
                logger.info("Using SSL for database connection.")

            # Initialize the engine
            self.engine = create_engine(
                self.DATABASE_URI,
                connect_args=connect_args,  # Pass SSL arguments if applicable
                echo=False  # SQLAlchemy logging for debugging
            )
            logger.info("Database engine initialized successfully.")

        except Exception as e:
            logger.error(f"Database connection initialization failed: {e}")
            raise e

    def create_session(self):
        try:
            # Create a session
            Session = sessionmaker(bind=self.engine)
            logger.info("Session created successfully.")
            return Session()
        except Exception as e:
            logger.error(f"Session creation failed: {e}")
            raise e

    def test_connection(self):
        try:
            # Test the database connection
            with self.engine.connect() as connection:
                logger.info("Database connection successful.")
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            raise e