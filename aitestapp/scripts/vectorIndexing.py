from aitestapp.scripts.config_functest import loadConfig
from aitestapp.scripts.docmentpar import WordDocumentParser
from aitestapp.scripts.model import ZhiPu4
from aitestapp.scripts.prompts import Prompts
import faiss
import numpy as np
from aitestapp.scripts.vectordb import VectorDatabase
from aitestapp import models
from django.conf import settings
import os
import logging

logger = logging.getLogger(__name__)

class VectorIndexing:
    def __init__(self, prd_name):
        self.config = loadConfig()
        self.configs = self.config.load_config()
        self.need_name = prd_name
        self.zhipu_ai = ZhiPu4()
        self.index = faiss.IndexFlatL2(1024)
        self.vector_id_to_text = []
        self.faiss_path_name = self.configs['FAISS_DB_PATH']
        self.host = self.configs['MYSQL_HOST']
        self.user = self.configs['MYSQL_USER']
        self.password = self.configs['MYSQL_PASSWORD']
        self.port = self.configs['MYSQL_PORT']
        self.db = self.configs['MYSQL_DATABASE']
        self.vectordb = VectorDatabase(self.host, self.user, self.password, self.port, self.db)

    def process_texts(self):
        prompt = Prompts()
        needs_text_list = []
        # 使用 settings 配置路径，避免硬编码
        base_data_dir = getattr(settings, 'DATA_DIR', os.path.join(settings.MEDIA_ROOT, 'data'))
        need_path = os.path.join(base_data_dir, self.need_name)
        parser = WordDocumentParser(need_path)
        sentences = parser.parse()
        needs_text_list.append(sentences)

        merged_needs_text_list = [sentence for sublist in needs_text_list for sentence in sublist]
        for text in merged_needs_text_list:
            need_text = prompt.analysis_requirements_prompt(text)
            reponse = self.zhipu_ai.zhipuai_request_vector(str(need_text))
            vector = reponse[1].data[0].embedding
            vector = np.array(vector).reshape(1, -1)
            self.index.add(vector)
            vector_id = self.index.ntotal - 1
            self.vector_id_to_text.append((vector_id + 1, text, vector_id))
            # 使用配置路径保存 FAISS 索引
            faiss_base_dir = getattr(settings, 'DATA_DIR', os.path.join(settings.MEDIA_ROOT, 'data'))
            faiss.write_index(self.index, os.path.join(faiss_base_dir, self.faiss_path_name))

        print('向量数据处理完毕')
        for id, text, vector_id in self.vector_id_to_text:
            data = self.vectordb.query_all()
            self.vectordb.create(id=1+len(data), text=text, vector_id=vector_id)

        print('数据关联存入数据库完毕')

    

