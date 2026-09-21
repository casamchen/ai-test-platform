import pymysql
import logging

logger = logging.getLogger(__name__)

class VectorDatabase:
    def __init__(self, host, user, password, port, db):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.db = db
        self.connection = None

    def connect(self):
        """创建数据库连接（每次操作新建连接，后续可优化为连接池）"""
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                db=self.db,
                port=self.port,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True,  # 自动提交，避免手动 commit
                connect_timeout=10  # 连接超时设置
            )
        except pymysql.Error as e:
            logger.error(f"数据库连接失败: {e}")
            raise

    def close(self):
        if self.connection:
            try:
                self.connection.close()
            except pymysql.Error as e:
                logger.warning(f"数据库连接关闭异常: {e}")
            finally:
                self.connection = None

    def create(self, id, vector_id, text):
        """插入向量数据"""
        self.connect()
        try:
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO aitestapp_vectors (id, vector_id, text) VALUES (%s, %s, %s)"
                cursor.execute(sql, (id, vector_id, text))
        except pymysql.Error as e:
            logger.error(f"插入向量数据失败: {e}")
            raise
        finally:
            self.close()

    def delete(self, vector_ids):
        """
        安全地删除向量数据，使用参数化查询防止SQL注入
        Args:
            vector_ids: 要删除的向量ID列表
        """
        if not vector_ids:
            return

        self.connect()
        try:
            with self.connection.cursor() as cursor:
                # 使用参数化查询，每个 %s 对应一个 ID
                placeholders = ', '.join(['%s'] * len(vector_ids))
                sql = f"DELETE FROM aitestapp_vectors WHERE vector_id IN ({placeholders})"
                cursor.execute(sql, tuple(vector_ids))  # 使用元组传参，确保参数化查询
        except pymysql.Error as e:
            logger.error(f"删除向量数据失败: {e}")
            raise
        finally:
            self.close()

    def query(self, vector_ids):
        """根据向量ID列表查询数据"""
        if not vector_ids:
            return []

        self.connect()
        try:
            with self.connection.cursor() as cursor:
                # 参数化查询防止注入
                placeholders = ', '.join(['%s'] * len(vector_ids))
                sql = f"SELECT * FROM aitestapp_vectors WHERE vector_id IN ({placeholders})"
                cursor.execute(sql, tuple(vector_ids))
                result = cursor.fetchall()
            return result
        except pymysql.Error as e:
            logger.error(f"查询向量数据失败: {e}")
            raise
        finally:
            self.close()

    def query_all(self):
        """查询所有向量文本数据"""
        self.connect()
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT text FROM aitestapp_vectors"
                cursor.execute(sql)
                result = cursor.fetchall()
            return result
        except pymysql.Error as e:
            logger.error(f"查询所有向量数据失败: {e}")
            raise
        finally:
            self.close()

    def create_needs_text(self, text, needs):
        """插入需求数据"""
        self.connect()
        try:
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO aitestapp_requirements (text, needs) VALUES (%s, %s)"
                cursor.execute(sql, (text, needs))
        except pymysql.Error as e:
            logger.error(f"插入需求数据失败: {e}")
            raise
        finally:
            self.close()

