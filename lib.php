<?php
/**
 * CURL实现GET或POST请求
 * @param $url          请求地址
 * @param $mode         请求方式（GET/POST）
 * @param $data         请求参数，执行POST请求时需要
 * @return object       返回对象数据包
 */
function sendReq($url, $data = array(), $mode = 'GET'){
	// 初始化
	$curl = curl_init();
	// 访问的URL
	curl_setopt($curl, CURLOPT_URL, $url);
	// 只获取页面内容，但不输出
	curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
	// 验证是否是https请求
	if(substr($url, 0, 5) == 'https'){
		// https请求，不验证证书
		curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
		// https请求，不验证HOST
		curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
	}
	if($mode == 'POST'){
		// 设置请求方式为POST请求
		curl_setopt($curl, CURLOPT_POST, true);
		// POST请求数据
		curl_setopt($curl, CURLOPT_POSTFIELDS, $data);
	}
	// 执行CURL请求
	$result = curl_exec($curl);
	// 关闭curl，释放资源
	curl_close($curl);
	return $result;
}

/**
 * 获取当前时间戳，精确到毫秒
 * @return float
 */
function microtime_float()
{
    list($usec, $sec) = explode(" ", microtime());
    return ((float)$usec + (float)$sec);
}

function xmlToJSON($content){
    $dir_name = "cache/".date("Y-m-d");
    $cache_name = $dir_name."/".microtime_float();

    if(!is_dir($dir_name)){
        mkdir($dir_name);
    }

    $xml = $content;

    file_put_contents("$cache_name".".xml", $xml);

    $json = json_encode(simplexml_load_file($cache_name.".xml"));
    file_put_contents("$cache_name".".json", $json);
    return $json;
}