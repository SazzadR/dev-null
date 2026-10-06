import { ArgumentMetadata, PipeTransform, UnprocessableEntityException } from '@nestjs/common';
import { AddressDto } from './address.dto.js';

export class AddressValidationPipe implements PipeTransform<AddressDto> {
  statePostCodeMap: Record<string, string> = {
    NSW: '2',
    VIC: '3',
    QLD: '4',
    SA: '5',
    WA: '6',
    TAS: '7',
  };

  transform(value: AddressDto, metadata: ArgumentMetadata) {
    if (!this.statePostCodeMap[value.state.toUpperCase()]) {
      throw new UnprocessableEntityException('Incorrect State Code');
    }
    if (
      this.statePostCodeMap[value.state.toUpperCase()].substring(0, 1) !== value.postCode.toString().substring(0, 1)
    ) {
      throw new UnprocessableEntityException(`The postcode ${value.postCode} does not match with state: ${value.state}`);
    }
    return value;
  }
}
