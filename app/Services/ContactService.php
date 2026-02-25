<?php

namespace App\Services;

use App\Models\Contact;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Pagination\LengthAwarePaginator;

class ContactService
{
    /**
     * Get paginated contacts for admin listing.
     */
    public function getAll(int $perPage = 15): LengthAwarePaginator
    {
        return Contact::ordered()->latest()->paginate($perPage);
    }

    /**
     * Get all active contacts (for public display).
     */
    public function getActiveContacts(): Collection
    {
        return Contact::active()->ordered()->get();
    }

    /**
     * Find a contact by ID.
     */
    public function findById(int $id): Contact
    {
        return Contact::findOrFail($id);
    }

    /**
     * Create a new contact.
     */
    public function create(array $data): Contact
    {
        return Contact::create($data);
    }

    /**
     * Update an existing contact.
     */
    public function update(int $id, array $data): Contact
    {
        $contact = $this->findById($id);
        $contact->update($data);

        return $contact->fresh();
    }

    /**
     * Delete a contact.
     */
    public function delete(int $id): void
    {
        $this->findById($id)->delete();
    }
}
