#ifndef channel_list_h
#define channel_list_h


#include "channel.h"


// Structs

typedef struct ChannelList ChannelList;


// Functions

/*
 * Creates a new channel list.
 *
 * Returns:
 * A new, empty channel list.
 */
ChannelList* init_channel_list();


/*
 * Adds a new channel to the channel list.
 *
 * Keyword arguments:
 * channel_list -- The list of channels to which to add the new channel.
 * channel -- The channel to add.
 */
void add_channel(ChannelList* channel_list, Channel* channel);


/*
 * Removes a channel from the list.
 *
 * Keyword arguments:
 * channel_list -- The list of channels from which to remove the channel.
 * name -- The name of the channel to remove.
 */
Channel* remove_channel(ChannelList* channel_list, char* name);


/*
 * Gets a channel by name.
 *
 * Keyword arguments:
 * channel_list -- The list of channels to search.
 * name -- The name of the channel to get.
 *
 * Returns:
 * A pointer to the channel with that name, or NULL if one is not found.
 */
Channel* get_channel(ChannelList* channel_list, char* name);


/*
 * Deallocates a list of channels and every channel in it. Sets the pointer to the channel list to NULL.
 *
 * Keyword arguments:
 * channel_list -- The channel list to destroy.
 */
void destroy_channel_list(ChannelList** channel_list);



#endif /* channel_list_h */
