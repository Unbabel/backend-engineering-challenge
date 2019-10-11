package com.chris.unbabel.handler;

import com.fasterxml.jackson.jaxrs.json.JacksonJsonProvider;
import org.glassfish.jersey.client.ClientConfig;

import javax.annotation.Nonnull;
import javax.ws.rs.client.Client;
import javax.ws.rs.client.ClientBuilder;
import javax.ws.rs.client.Entity;
import javax.ws.rs.core.GenericType;
import javax.ws.rs.core.MediaType;
import java.util.Collection;

public class RestServiceInvoker<I, O> {
    private final String endPoint;
    private Client client;

    public RestServiceInvoker(@Nonnull final String endPoint) {
        this.endPoint = endPoint;

        ClientConfig config = new ClientConfig();
        config.register(JacksonJsonProvider.class);
        client = ClientBuilder.newClient(config);
    }

    public Collection<O> call(I payload) {
        return client
                .target(endPoint)
                .request(MediaType.APPLICATION_JSON)
                .post(Entity.entity(payload, MediaType.APPLICATION_JSON))
                .readEntity(new GenericType<Collection<O>>() {
                });
    }
}