import { Body, Controller, Get, Param, Post } from '@nestjs/common';
import { CreateMessageDto } from './dto.js';

@Controller('messages')
export class MessagesController {
  @Get()
  listMessages(): { id: number; message: string }[] {
    return [
      {
        id: 1,
        message: 'message 1',
      },
    ];
  }

  @Get(':id')
  getMessage(@Param('id') id: number): { id: number; message: string } {
    return {
      id: id,
      message: 'message 1',
    };
  }

  @Post()
  createMessage(@Body() createMessageDto: CreateMessageDto) {
    console.log(createMessageDto);
    return 'Message created successfully.';
  }
}
