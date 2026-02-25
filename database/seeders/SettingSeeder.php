<?php

namespace Database\Seeders;

use App\Models\Setting;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;

class SettingSeeder extends Seeder
{
    use WithoutModelEvents;

    public function run(): void
    {
        $aboutUsData = [
            'hero' => [
                'tagline'          => 'Câu chuyện của chúng tôi',
                'headline'         => 'Học ngôn ngữ qua',
                'headline_gradient'=> 'những tầm cao nhân loại.',
                'description'      => '"The Admirable" ra đời mang theo một sứ mệnh: Biến quá trình học tiếng Anh đầy gian nan trở thành một hành trình tận hưởng những giá trị tốt đẹp nhất của tri thức.',
            ],
            'stats' => [
                ['value' => '50+',  'label' => 'Nhân vật vĩ đại'],
                ['value' => '8',    'label' => 'Lĩnh vực đa dạng'],
                ['value' => '200+', 'label' => 'Bài đọc song ngữ'],
                ['value' => '100%', 'label' => 'Miễn phí, mãi mãi'],
            ],
            'problem' => [
                'title'       => 'Nỗi trăn trở của người học',
                'description' => 'Chúng tôi thấu hiểu rằng việc học IELTS hay nâng cao vốn tiếng Anh thường đi kèm với những bài báo học thuật khô khan, phức tạp. Người học rất dễ cảm thấy chán nản, buồn ngủ và gặp khó khăn trong việc ghi nhớ từ vựng cũng như duy trì động lực mỗi ngày.',
            ],
            'solution' => [
                'title'       => 'Giải pháp mang tên "The Admirable"',
                'description' => 'Thay vì ép bản thân đọc những nội dung vô hồn, chúng tôi cung cấp các bài viết song ngữ chất lượng cao kể về những tấm gương vĩ đại trên toàn thế giới—từ văn hóa, kinh tế, khoa học đến chính trị.',
                'bullets'     => [
                    'Nội dung truyền cảm hứng, tích cực và sâu sắc.',
                    'Hệ sinh thái đa phương tiện: Text, Audio, Video YouTube.',
                    'Ghi nhớ từ vựng tự nhiên thông qua bối cảnh câu chuyện.',
                ],
            ],
            'core_values' => [
                'tagline' => 'Giá trị cốt lõi',
                'title'   => 'Những gì chúng tôi tin tưởng',
                'items'   => [
                    ['title' => 'Tri thức mở',       'description' => 'Mọi nội dung đều miễn phí, không cần đăng ký, không paywall. Kiến thức là quyền của tất cả.'],
                    ['title' => 'Chất lượng cao',     'description' => 'Bài viết được biên soạn kỹ lưỡng, song ngữ chuẩn xác, đúng ngữ pháp và phù hợp IELTS.'],
                    ['title' => 'Truyền cảm hứng',   'description' => 'Nội dung tích cực, khơi dậy động lực học tập và tinh thần vươn lên từ các tấm gương.'],
                    ['title' => 'Đa dạng lĩnh vực',  'description' => 'Từ khoa học, chính trị, nghệ thuật đến thể thao — phủ sóng mọi góc nhìn về nhân loại.'],
                ],
            ],
            'audience' => [
                'title'       => 'Nền tảng này dành cho ai?',
                'description' => 'Không cần tạo tài khoản rườm rà. Hệ thống được mở hoàn toàn công khai để mang tri thức đến với tất cả mọi người.',
                'items'       => [
                    ['title' => 'Người học IELTS',     'description' => 'Đắm chìm trong từ vựng cao cấp (Advanced Vocabulary) và cấu trúc câu phức tạp một cách tự nhiên qua các bài viết học thuật mang tính tiểu sử.'],
                    ['title' => 'Người yêu tiếng Anh', 'description' => 'Cải thiện cả hai kỹ năng Reading và Listening đồng thời thông qua các bài đọc song ngữ kèm giọng đọc audio chuẩn xác.'],
                    ['title' => 'Người tìm cảm hứng', 'description' => 'Dành cho bất cứ ai muốn tìm kiếm năng lượng tích cực, sự kiên cường và động lực từ những con người đã làm thay đổi thế giới.'],
                ],
            ],
            'cta' => [
                'quote'       => 'Đọc là để sống nhiều hơn một lần.',
                'headline'    => 'Sẵn sàng để bắt đầu?',
                'description' => 'Hãy khám phá những câu chuyện đã truyền cảm hứng cho hàng triệu người trên thế giới — hoàn toàn miễn phí.',
            ],
        ];

        Setting::setValue('about_us_data', json_encode($aboutUsData, JSON_UNESCAPED_UNICODE));
    }
}
