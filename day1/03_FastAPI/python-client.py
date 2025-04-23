# python_client.py
# このコードは、ngrokで公開されたAPIにアクセスするPythonクライアントの例です

import requests
import json
import time

class LLMClient:
    """LLM API クライアントクラス"""
    
    def __init__(self, api_url):
        """
        初期化
        
        Args:
            api_url (str): API のベース URL（ngrok URL）
        """
        self.api_url = api_url.rstrip('/')
        self.session = requests.Session()
    
    def health_check(self):
        """
        ヘルスチェック
        
        Returns:
            dict: ヘルスチェック結果
        """
        response = self.session.get(f"{self.api_url}/health")
        return response.json()
    
    def get_model_name(self):
        """
        Get the configured model name from the API
        
        Returns:
            dict: API response containing the model name
        """
        response = self.session.get(f"{self.api_url}/model")
        return response.json()
    
    def get_fortune(self):
        """
        Get a random fortune from the API

        Returns:
            dict: API response containing the fortune message
        """
        response = self.session.get(f"{self.api_url}/fortune")
        return response.json()
    
    def generate(self, prompt, max_new_tokens=512, temperature=0.7, top_p=0.9, do_sample=True):
        """
        テキスト生成
        
        Args:
            prompt (str): プロンプト文字列
            max_new_tokens (int, optional): 生成する最大トークン数
            temperature (float, optional): 温度パラメータ
            top_p (float, optional): top-p サンプリングのパラメータ
            do_sample (bool, optional): サンプリングを行うかどうか
        
        Returns:
            dict: 生成結果
        """
        payload = {
            "prompt": prompt,
            "max_new_tokens": max_new_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "do_sample": do_sample
        }
        
        start_time = time.time()
        response = self.session.post(
            f"{self.api_url}/generate",
            json=payload
        )
        total_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            result["total_request_time"] = total_time
            return result
        else:
            raise Exception(f"API error: {response.status_code} - {response.text}")

# 使用例
if __name__ == "__main__":
    # ngrok URLを設定（実際のURLに置き換えてください）
    NGROK_URL = "https://your-ngrok-url.ngrok.url"
    
    # クライアントの初期化
    client = LLMClient(NGROK_URL)
    
    # ヘルスチェック
    print("Health check:")
    print(client.health_check())
    print()

    # Get model name
    print("Get model name:")
    model_info = client.get_model_name()
    print(f"Model served by API: {model_info.get('model_name', 'N/A')}")
    print()

    # Get a fortune
    print("Your fortune for today:")
    fortune_info = client.get_fortune()
    print(f">>> {fortune_info.get('fortune', 'Could not fetch fortune.')}")
    print()
    
    # 単一の質問
    print("Simple question:")
    result = client.generate([
        {"prompt": "AIについて100文字で教えてください"}
    ])
    print(f"Response: {result['generated_text']}")
    print(f"Model processing time: {result['response_time']:.2f}s")
    print(f"Total request time: {result['total_request_time']:.2f}s")    