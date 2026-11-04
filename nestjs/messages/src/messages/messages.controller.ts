import {
  Body,
  Controller,
  Get,
  NotFoundException,
  Param,
  Post,
} from '@nestjs/common';
import { CreateMessageDto } from './dto.js';
import { MessagesService } from './messages.service.js';
import type { MessageInterface } from './message.interface.js';

@Controller('messages')
export class MessagesController {
  constructor(public messagesService: MessagesService) {}

  @Get()
  listMessages(): Promise<MessageInterface[]> {
    return this.messagesService.listMessages();
  }

  @Get(':id')
  async getMessage(@Param('id') id: string): Promise<MessageInterface> {
    const message = await this.messagesService.getMessage(id);
    if (!message) {
      throw new NotFoundException();
    }

    return message;
  }

  @Post()
  createMessage(@Body() createMessageDto: CreateMessageDto): Promise<MessageInterface> {
    return this.messagesService.createMessage(createMessageDto);
  }
}
