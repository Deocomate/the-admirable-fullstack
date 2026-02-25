<?php

namespace Database\Seeders;

use App\Models\Category;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;

class CategorySeeder extends Seeder
{
    use WithoutModelEvents;

    public function run(): void
    {
        $categories = [
            ['name' => 'Tội phạm & Pháp luật (Crime & Law)', 'slug' => 'toi-pham-phap-luat-crime-law'],
            ['name' => 'Môi trường (Environment)',            'slug' => 'moi-truong-environment'],
            ['name' => 'Lịch sử (History)',                   'slug' => 'lich-su-history'],
            ['name' => 'Truyền thông (Media & Communication)','slug' => 'truyen-thong-media-communication'],
            ['name' => 'Sức khỏe & Y tế (Health & Medicine)', 'slug' => 'suc-khoe-y-te-health-medicine'],
            ['name' => 'Giáo dục (Education)',                'slug' => 'giao-duc-education'],
            ['name' => 'Chính trị',                           'slug' => 'chinh-tri'],
            ['name' => 'Khoa học',                            'slug' => 'khoa-hoc'],
            ['name' => 'Nghệ thuật',                          'slug' => 'nghe-thuat'],
            ['name' => 'Kinh tế',                             'slug' => 'kinh-te'],
            ['name' => 'Thể thao',                            'slug' => 'the-thao'],
            ['name' => 'Công nghệ',                           'slug' => 'cong-nghe'],
            ['name' => 'Văn hóa',                             'slug' => 'van-hoa'],
            ['name' => 'Đời sống',                            'slug' => 'doi-song'],
        ];

        foreach ($categories as $cat) {
            Category::firstOrCreate(
                ['slug' => $cat['slug']],
                ['name' => $cat['name']]
            );
        }
    }
}
