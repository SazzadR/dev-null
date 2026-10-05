import { ApiProperty, OmitType } from '@nestjs/swagger';

export class AddressDto {
  @ApiProperty({ description: 'Unique identifier of the address', example: 1, type: 'integer' })
  id: number;

  @ApiProperty({ description: 'Street address', example: '123 Queen Street' })
  addressLine: string;

  @ApiProperty({ description: 'Postal code', example: 4000, type: 'integer' })
  postCode: number;

  @ApiProperty({ description: 'State or region code', example: 'QLD' })
  state: string;

  @ApiProperty({
    description: 'Date and time when the address was created',
    example: '2026-10-06T08:30:00.000Z',
    type: String,
    format: 'date-time',
  })
  createdAt: Date;
}

export class CreateAddressDto extends OmitType(AddressDto, ['id', 'createdAt']) {}

export class UpdateAddressDto extends OmitType(AddressDto, ['id', 'createdAt']) {}
