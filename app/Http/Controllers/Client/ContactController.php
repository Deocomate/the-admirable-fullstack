<?php

namespace App\Http\Controllers\Client;

use App\Http\Controllers\Controller;
use App\Services\ContactService;

class ContactController extends Controller
{
    /**
     * Display the Contact page.
     */
    public function index()
    {
        $contactService = new ContactService();
        $contacts = $contactService->getActiveContacts();

        return view('client.contact.index', compact('contacts'));
    }
}
