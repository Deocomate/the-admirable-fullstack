<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Http\Requests\StoreContactRequest;
use App\Http\Requests\UpdateContactRequest;
use App\Services\ContactService;
use Illuminate\Http\RedirectResponse;
use Illuminate\View\View;

class ContactController extends Controller
{
    public function __construct(private readonly ContactService $contactService) {}

    /**
     * Display a listing of contacts.
     */
    public function index(): View
    {
        $contacts = $this->contactService->getAll();

        return view('admin.contacts.index', compact('contacts'));
    }

    /**
     * Show the form for creating a new contact.
     */
    public function create(): View
    {
        return view('admin.contacts.form');
    }

    /**
     * Store a newly created contact.
     */
    public function store(StoreContactRequest $request): RedirectResponse
    {
        $data = $request->validated();
        $data['is_active'] = $request->boolean('is_active', true);

        $this->contactService->create($data);

        return redirect()->route('admin.contacts.index')
            ->with('success', 'Thông tin liên hệ đã được tạo thành công.');
    }

    /**
     * Show the form for editing a contact.
     */
    public function edit(int $contact): View
    {
        $contact = $this->contactService->findById($contact);

        return view('admin.contacts.form', compact('contact'));
    }

    /**
     * Update the specified contact.
     */
    public function update(UpdateContactRequest $request, int $contact): RedirectResponse
    {
        $data = $request->validated();
        $data['is_active'] = $request->boolean('is_active', true);

        $this->contactService->update($contact, $data);

        return redirect()->route('admin.contacts.index')
            ->with('success', 'Thông tin liên hệ đã được cập nhật thành công.');
    }

    /**
     * Remove the specified contact.
     */
    public function destroy(int $contact): RedirectResponse
    {
        try {
            $this->contactService->delete($contact);
        } catch (\Exception $e) {
            return redirect()->route('admin.contacts.index')
                ->with('error', 'Không thể xóa liên hệ: ' . $e->getMessage());
        }

        return redirect()->route('admin.contacts.index')
            ->with('success', 'Thông tin liên hệ đã được xóa thành công.');
    }
}
