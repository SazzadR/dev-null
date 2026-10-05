import { OmitType } from '@nestjs/mapped-types';

export class AddressDto {
  id: number;
  addressLine: string;
  postCode: number;
  state: string;
  createdAt: Date;
}

export class CreateAddressDto extends OmitType(AddressDto, ['id', 'createdAt']) {}

export class UpdateAddressDto extends OmitType(AddressDto, ['id', 'createdAt']) {}