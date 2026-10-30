import { Controller, Get } from '@nestjs/common';

@Controller()
export class AppController {
  @Get()
  public index(): string {
    return 'Hello World!';
  }
}
