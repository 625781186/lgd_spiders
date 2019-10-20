from db.DBInterface import DBInterface

from ip.IpVerify import testBaidu
# from ip.IpVerify import test_qccM
# from ip.IpVerify import testZhuanli

# tyc_ip = DBInterface(col="tyc_ip", input_verify=test_tyc, forVerify=testBaidu, describe="天眼查")

#pools池里面存放着多个实例化的对象，接收4个参数，第一个是数据库表名，第二个参数和第三个参数一样都是ip的验证返回值不是True就是False,最后一个参数是日志
pools = [
    # DBInterface(col="qcc_m_ip", input_verify=test_qccM, forVerify=testBaidu, describe='企查查m端'),
    DBInterface(col="testIpProxy", input_verify=testBaidu, forVerify=testBaidu, describe='百度'),
    # DBInterface(col="wusong_ip", input_verify=wusong, forVerify=testBaidu, describe='无讼'),
    # DBInterface(col="zhigaodian_ip", input_verify=zhigaodian, forVerify=testBaidu, describe='制高点'),
    # DBInterface(col="zhuanli_ip", input_verify=testZhuanli, forVerify=testBaidu, describe='专利'),
    #testIpProxy   为ip池的表明，input_verify为获取ip池的第一步入库前的验证，forVerify为持续验证ip是否过期
]
