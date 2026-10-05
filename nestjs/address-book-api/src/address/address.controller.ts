import {
  Body,
  Controller, Delete,
  Get,
  NotFoundException,
  Param,
  ParseIntPipe,
  Post, Put,
} from '@nestjs/common';
import { AddressService } from './address.service.js';
import { CreateAddressDto, UpdateAddressDto } from './address.dto.js';

@Controller('address')
export class AddressController {
  constructor(private readonly addressService: AddressService) {}

  @Get()
  getAll() {
    return this.addressService.getAll();
  }

  @Get(':id')
  getById(@Param('id', ParseIntPipe) id: number) {
    const address = this.addressService.getById(id);
    if (!address) {
      throw new NotFoundException('Address not found');
    }
    return address;
  }

  @Post()
  create(@Body() address: CreateAddressDto) {
    return this.addressService.create(address);
  }

  @Put(':id')
  update(@Param('id', ParseIntPipe) id: number, @Body() address: UpdateAddressDto) {
    const updatedAddress = this.addressService.update(id, address);
    if (!updatedAddress) {
      throw new NotFoundException('Address not found');
    }
    return updatedAddress;
  }

  @Delete(':id')
  delete(@Param('id', ParseIntPipe) id: number) {
    const deletedAddress = this.addressService.delete(id);
    if (!deletedAddress) {
      throw new NotFoundException('Address not found');
    }
  }
}
