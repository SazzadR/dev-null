import { Injectable } from '@nestjs/common';
import { AddressDto, CreateAddressDto, UpdateAddressDto } from './address.dto.js';

@Injectable()
export class AddressService {
  private addressData: AddressDto[] = [
    {
      id: 1,
      addressLine: '123 Queen Street',
      postCode: 4000,
      state: 'QLD',
      createdAt: new Date(),
    },
    {
      id: 2,
      addressLine: '456 Long Island',
      postCode: 5000,
      state: 'LIL',
      createdAt: new Date(),
    },
  ];

  getAll(): AddressDto[] {
    return this.addressData;
  }

  getById(id: number): AddressDto | undefined {
    return this.addressData.find((address) => address.id === id);
  }

  create(address: CreateAddressDto): AddressDto {
    const id = this.addressData.length === 0 ? 0 : Math.max(...this.addressData.map((address) => address.id));
    const newAddress = { ...address, id: id + 1, createdAt: new Date() };
    this.addressData.push(newAddress);
    return newAddress;
  }

  update(id: number, address: UpdateAddressDto): AddressDto | undefined {
    const index = this.addressData.findIndex((address) => address.id === id);
    if (index === -1) {
      return;
    }
    const addressToUpdate = this.addressData[index];
    addressToUpdate.addressLine = address.addressLine;
    addressToUpdate.postCode = address.postCode;
    addressToUpdate.state = address.state;
    this.addressData[index] = addressToUpdate;
    return addressToUpdate;
  }

  delete(id: number): AddressDto | undefined {
    const index = this.addressData.findIndex((address) => address.id === id);
    if (index === -1) {
      return;
    }
    const addressToDelete = this.addressData[index];
    this.addressData.splice(index, 1);
    return addressToDelete;
  }
}
