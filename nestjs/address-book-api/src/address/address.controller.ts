import {
  Body,
  Controller,
  Delete,
  Get,
  HttpCode,
  HttpStatus,
  NotFoundException,
  Param,
  ParseIntPipe,
  Post,
  Put,
  UsePipes,
} from '@nestjs/common';
import {
  ApiBadRequestResponse,
  ApiBody,
  ApiCreatedResponse,
  ApiNoContentResponse,
  ApiNotFoundResponse,
  ApiOkResponse,
  ApiOperation,
  ApiParam,
  ApiTags,
} from '@nestjs/swagger';
import { AddressService } from './address.service.js';
import { AddressDto, CreateAddressDto, UpdateAddressDto } from './address.dto.js';
import { AddressValidationPipe } from './address.validation.js';

@ApiTags('Address')
@Controller('address')
export class AddressController {
  constructor(private readonly addressService: AddressService) {}

  @ApiOperation({ summary: 'Get all addresses' })
  @ApiOkResponse({
    description: 'Addresses retrieved successfully',
    type: AddressDto,
    isArray: true,
  })
  @Get()
  getAll() {
    return this.addressService.getAll();
  }

  @ApiParam({
    name: 'id',
    description: 'Address ID',
    required: true,
    type: 'integer',
    example: 1,
  })
  @ApiOperation({ summary: 'Get an address by ID' })
  @ApiOkResponse({ description: 'Address retrieved successfully', type: AddressDto })
  @ApiBadRequestResponse({ description: 'The address ID is not a valid integer' })
  @ApiNotFoundResponse({ description: 'Address not found' })
  @Get(':id')
  getById(@Param('id', ParseIntPipe) id: number) {
    const address = this.addressService.getById(id);
    if (!address) {
      throw new NotFoundException('Address not found');
    }
    return address;
  }

  @ApiOperation({ summary: 'Create an address' })
  @ApiBody({ type: CreateAddressDto })
  @ApiCreatedResponse({ description: 'Address created successfully', type: AddressDto })
  @UsePipes(AddressValidationPipe)
  @Post()
  create(@Body() address: CreateAddressDto) {
    return this.addressService.create(address);
  }

  @ApiParam({
    name: 'id',
    description: 'Address ID',
    required: true,
    type: 'integer',
    example: 1,
  })
  @ApiOperation({ summary: 'Update an address' })
  @ApiBody({ type: UpdateAddressDto })
  @ApiOkResponse({ description: 'Address updated successfully', type: AddressDto })
  @ApiBadRequestResponse({ description: 'The address ID is not a valid integer' })
  @ApiNotFoundResponse({ description: 'Address not found' })
  @Put(':id')
  update(@Param('id', ParseIntPipe) id: number, @Body() address: UpdateAddressDto) {
    const updatedAddress = this.addressService.update(id, address);
    if (!updatedAddress) {
      throw new NotFoundException('Address not found');
    }
    return updatedAddress;
  }

  @ApiParam({
    name: 'id',
    description: 'Address ID',
    required: true,
    type: 'integer',
    example: 1,
  })
  @ApiOperation({ summary: 'Delete an address' })
  @ApiNoContentResponse({ description: 'Address deleted successfully' })
  @ApiBadRequestResponse({ description: 'The address ID is not a valid integer' })
  @ApiNotFoundResponse({ description: 'Address not found' })
  @Delete(':id')
  @HttpCode(HttpStatus.NO_CONTENT)
  delete(@Param('id', ParseIntPipe) id: number) {
    const deletedAddress = this.addressService.delete(id);
    if (!deletedAddress) {
      throw new NotFoundException('Address not found');
    }
  }
}
