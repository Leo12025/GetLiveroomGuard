# 获取B站直播间舰长列表工具

import requests
import argparse
import json
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, Alignment

# 设置请求头，模拟浏览器访问
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'Referer': 'https://live.bilibili.com/',
    'Cookie': 'SESSDATA=your_sessdata_here; bili_jct=your_bili_jct_here'  # 需要替换为实际的Cookie
}

# B站API基础URL
BASE_URL = 'https://api.live.bilibili.com'

class BiliBiliLiveGuard:
    def __init__(self, room_id):
        self.room_id = room_id
        self.guard_list = []

    def get_guard_info(self):
        """获取直播间舰长信息"""
        url = f'{BASE_URL}/xlive/app-room/v2/guardTab/guardList'
        params = {
            'roomid': self.room_id,
            'page': 1,
            'page_size': 30  # 每页获取30条数据
        }

        try:
            response = requests.get(url, headers=HEADERS, params=params)
            if response.status_code == 200:
                data = response.json()
                if data['code'] == 0:
                    # 处理分页
                    total_page = data['data']['page_info']['total_page']
                    self._process_guard_data(data['data']['list'])

                    # 获取后续页面数据
                    for page in range(2, total_page + 1):
                        params['page'] = page
                        page_response = requests.get(url, headers=HEADERS, params=params)
                        if page_response.status_code == 200:
                            page_data = page_response.json()
                            if page_data['code'] == 0:
                                self._process_guard_data(page_data['data']['list'])
                            else:
                                print(f'获取第{page}页数据失败: {page_data.get("message", "未知错误")}')
                        else:
                            print(f'请求第{page}页失败，状态码: {page_response.status_code}')

                    return True
                else:
                    print(f'API返回错误: {data.get("message", "未知错误")}')
                    return False
            else:
                print(f'请求失败，状态码: {response.status_code}')
                return False
        except Exception as e:
            print(f'发生异常: {str(e)}')
            return False

    def _process_guard_data(self, guard_data):
        """处理舰长数据"""
        for guard in guard_data:
            # 提取所需信息
            user_info = {
                '用户名': guard['username'],
                'uid': guard['uid'],
                '舰长等级': self._get_guard_level(guard['guard_level']),
                '勋章等级': guard['medal_info']['medal_level'] if guard.get('medal_info') else 0,
                '消费': f'{guard["price"] / 1000:.1f}元'  # 转换为元
            }
            self.guard_list.append(user_info)

    def _get_guard_level(self, level):
        """将数字等级转换为文字"""
        levels = {1: '总督', 2: '提督', 3: '舰长'}
        return levels.get(level, f'未知等级({level})')

    def print_guard_list(self):
        """打印舰长列表"""
        if not self.guard_list:
            print('未获取到舰长信息')
            return

        print(f'直播间 {self.room_id} 的舰长列表 ({len(self.guard_list)}人):')
        print('-' * 80)
        # 格式化输出表头
        print(f'{"用户名":<20}{"UID":<15}{"舰长等级":<10}{"勋章等级":<10}{"消费"}')
        print('-' * 80)

        # 打印每个舰长的信息
        for guard in self.guard_list:
            print(f'{guard["用户名"]:<20}{guard["uid"]:<15}{guard["舰长等级"]:<10}{guard["勋章等级"]:<10}{guard["消费"]}')

    def save_to_file(self, filename=None):
        """保存舰长列表到JSON文件"""
        if not self.guard_list:
            print('没有舰长信息可保存')
            return False

        if not filename:
            filename = f'guard_list_{self.room_id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.guard_list, f, ensure_ascii=False, indent=2)
            print(f'舰长信息已保存到 {filename}')
            return True
        except Exception as e:
            print(f'保存文件失败: {str(e)}')
            return False

    def save_to_excel(self, filename=None):
        """保存舰长列表到Excel文件"""
        if not self.guard_list:
            print('没有舰长信息可保存')
            return False

        if not filename:
            filename = f'guard_list_{self.room_id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'

        try:
            # 创建工作簿和工作表
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = '舰长列表'

            # 设置表头
            headers = ['用户名', 'UID', '舰长等级', '勋章等级', '消费']
            for col_idx, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col_idx)
                cell.value = header
                cell.font = Font(bold=True)
                cell.alignment = Alignment(horizontal='center', vertical='center')

            # 填充数据
            for row_idx, guard in enumerate(self.guard_list, 2):
                ws.cell(row=row_idx, column=1).value = guard['用户名']
                ws.cell(row=row_idx, column=2).value = guard['uid']
                ws.cell(row=row_idx, column=3).value = guard['舰长等级']
                ws.cell(row=row_idx, column=4).value = guard['勋章等级']
                ws.cell(row=row_idx, column=5).value = guard['消费']

            # 调整列宽
            for col in ws.columns:
                max_length = 0
                column = col[0].column_letter  # 获取列字母
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = (max_length + 2) * 1.2
                ws.column_dimensions[column].width = adjusted_width

            # 保存文件
            wb.save(filename)
            print(f'舰长信息已保存到Excel文件: {filename}')
            return True
        except Exception as e:
            print(f'保存Excel文件失败: {str(e)}')
            return False

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='获取B站直播间舰长列表')
    parser.add_argument('room_id', type=int, help='直播间ID')
    parser.add_argument('-o', '--output', help='输出文件名')
    parser.add_argument('-e', '--excel', action='store_true', help='导出为Excel格式')
    args = parser.parse_args()

    # 创建实例并获取舰长信息
    bili_guard = BiliBiliLiveGuard(args.room_id)
    if bili_guard.get_guard_info():
        # 打印舰长列表
        bili_guard.print_guard_list()

        # 保存到文件
        if args.output:
            if args.excel:
                bili_guard.save_to_excel(args.output)
            else:
                bili_guard.save_to_file(args.output)
        elif args.excel:
            bili_guard.save_to_excel()

if __name__ == '__main__':
    main()

# 使用说明:
# 1. 替换代码中的Cookie为你自己的B站Cookie
# 2. 运行命令: python get_liveroom_guard.py 直播间ID
# 3. 可选参数:
#    -o 文件名 保存舰长信息到指定文件
#    -e 导出为Excel格式 (与-o参数一起使用时将保存为Excel文件)