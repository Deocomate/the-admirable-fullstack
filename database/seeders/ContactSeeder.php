<?php

namespace Database\Seeders;

use App\Models\Contact;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;

class ContactSeeder extends Seeder
{
    use WithoutModelEvents;

    public function run(): void
    {
        $contacts = [
            [
                'type'       => 'email',
                'label'      => 'Email',
                'value'      => 'longnvm2003@gmail.com',
                'sort_order' => 1,
                'is_active'  => true,
            ],
            [
                'type'       => 'phone',
                'label'      => 'Số điện thoại',
                'value'      => '0865095066',
                'sort_order' => 2,
                'is_active'  => true,
            ],
            [
                'type'       => 'facebook',
                'label'      => 'Facebook',
                'value'      => 'https://facebook.com/',
                'sort_order' => 3,
                'is_active'  => true,
            ],
            [
                'type'       => 'github',
                'label'      => 'GitHub',
                'value'      => 'https://github.com/',
                'sort_order' => 4,
                'is_active'  => true,
            ],
            [
                'type'       => 'whatsapp',
                'label'      => 'WhatsApp',
                'value'      => 'https://wa.me/84865095066',
                'sort_order' => 5,
                'is_active'  => true,
            ],
        ];

        foreach ($contacts as $contact) {
            Contact::firstOrCreate(
                ['type' => $contact['type'], 'value' => $contact['value']],
                $contact
            );
        }
    }
}
