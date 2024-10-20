## 对支付宝 NFC 静态支付贴纸的研究
> 本项目仅用于学习使用，不可用于商业用途，侵删谢谢🙏。

### 贴纸数据
    数据主要有两块，一块是一段 https://，另一段是 External
#### https://
```
https://render.alipay.com/p/s/ulink/?scene=nfc&scheme=alipay%3A%2F%2Fnfc%2Fapp%3Fid%3D10000007%26actionType%3Droute%26codeContent%3Dhttps%253A%252F%252Fqr.alipay.com%252Ftsx17757hcbamrotqw2bp00%253FnoT%253Dntagtqp
```
#### External
```
com.eg.android.AlipayGphone
```

这段 https:// 经过测试，可以由普通的收款码进行生成，将对应的数据内容进行替换即可。详情可见 “generateNFC.py” 或 “generateNFC.html” 文件。

### 生成之后请自行测试收款效果